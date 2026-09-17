#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

function parseArgs(argv) {
  const options = {
    force: false,
    dryRun: false,
    list: false,
    only: null,
    concurrency: 1,
    config: "illustrations/config.json"
  };

  for (const arg of argv) {
    if (arg === "--force") options.force = true;
    else if (arg === "--dry-run") options.dryRun = true;
    else if (arg === "--list") options.list = true;
    else if (arg.startsWith("--only=")) {
      options.only = new Set(
        arg
          .slice("--only=".length)
          .split(",")
          .map((v) => v.trim())
          .filter(Boolean)
      );
    } else if (arg.startsWith("--concurrency=")) {
      const value = Number(arg.slice("--concurrency=".length));
      if (!Number.isInteger(value) || value < 1) {
        throw new Error("--concurrency must be a positive integer");
      }
      options.concurrency = value;
    } else if (arg.startsWith("--config=")) {
      options.config = arg.slice("--config=".length);
    } else if (arg === "--help" || arg === "-h") {
      console.log(`Usage: node scripts/generate_illustrations.mjs [options]\n\nOptions:\n  --dry-run            Show what would be generated without calling the API\n  --force              Regenerate even when an image already exists\n  --list               List parsed illustration entries and exit\n  --only=a,b           Generate only entries whose heading/title contains a or b\n  --concurrency=N      Number of concurrent generations (default: 1)\n  --config=PATH        Config JSON path (default: illustrations/config.json)\n  -h, --help           Show this help\n\nEnvironment:\n  MODELSLAB_API_KEY    Required unless --dry-run or --list is used\n  MODELSLAB_MODEL_ID   Optional override for config model_id\n`);
      process.exit(0);
    }
  }

  return options;
}

function sanitizeFilename(value) {
  return value
    .normalize("NFKC")
    .replace(/[\\/:*?"<>|]/g, "-")
    .replace(/[\u0000-\u001f]/g, "")
    .replace(/\s+/g, "_")
    .replace(/_+/g, "_")
    .replace(/-+/g, "-")
    .replace(/^[-_.]+|[-_.]+$/g, "")
    .slice(0, 120);
}

function stripLegacyStyle(prompt, fragments = []) {
  let result = prompt;
  for (const fragment of fragments) {
    if (!fragment) continue;
    result = result.replaceAll(fragment, "");
  }
  return result
    .replace(/\s*,\s*,+/g, ", ")
    .replace(/^\s*,\s*|\s*,\s*$/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function extractCodeBlock(body, label) {
  const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const re = new RegExp(`\\*\\*${escaped}\\*\\*\\s*\\n+\\`\\`\\`(?:text)?\\s*\\n([\\s\\S]*?)\\n\\`\\`\\``, "i");
  const match = body.match(re);
  return match ? match[1].trim() : null;
}

function parsePromptMarkdown(markdown) {
  const headingRe = /^###\s+(.+)$/gm;
  const headings = [...markdown.matchAll(headingRe)];
  const entries = [];

  for (let i = 0; i < headings.length; i += 1) {
    const heading = headings[i][1].trim();
    const start = headings[i].index + headings[i][0].length;
    const end = i + 1 < headings.length ? headings[i + 1].index : markdown.length;
    const body = markdown.slice(start, end);

    const positive = extractCodeBlock(body, "Positive prompt");
    const negative = extractCodeBlock(body, "Negative prompt");
    if (!positive || !negative) continue;

    const separator = heading.indexOf(" — ");
    const date = separator >= 0 ? heading.slice(0, separator).trim() : "undated";
    const title = separator >= 0 ? heading.slice(separator + 3).trim() : heading;
    const baseName = sanitizeFilename(`${date}_${title}`);

    entries.push({ heading, date, title, positive, negative, baseName });
  }

  return entries;
}

async function fileExists(file) {
  try {
    await fs.access(file);
    return true;
  } catch {
    return false;
  }
}

async function findExistingImage(basePath) {
  for (const ext of [".png", ".jpg", ".jpeg", ".webp"]) {
    const candidate = `${basePath}${ext}`;
    if (await fileExists(candidate)) return candidate;
  }
  return null;
}

function extensionFromContentType(contentType, url) {
  if (contentType?.includes("image/png")) return ".png";
  if (contentType?.includes("image/webp")) return ".webp";
  if (contentType?.includes("image/jpeg")) return ".jpg";

  try {
    const ext = path.extname(new URL(url).pathname).toLowerCase();
    if ([".png", ".webp", ".jpg", ".jpeg"].includes(ext)) return ext;
  } catch {
    // Ignore invalid URL here; download will report the real error.
  }

  return ".png";
}

async function postJson(url, body) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });

  const text = await response.text();
  let json;
  try {
    json = JSON.parse(text);
  } catch {
    throw new Error(`ModelsLab returned non-JSON (${response.status}): ${text.slice(0, 500)}`);
  }

  if (!response.ok) {
    throw new Error(`ModelsLab HTTP ${response.status}: ${JSON.stringify(json).slice(0, 1000)}`);
  }

  return json;
}

async function waitForOutputs(initial, apiKey, config) {
  let data = initial;

  for (let attempt = 0; attempt <= config.max_poll_attempts; attempt += 1) {
    if (data.status === "success" && Array.isArray(data.output) && data.output.length > 0) {
      return data.output;
    }

    if (Array.isArray(data.output) && data.output.length > 0) {
      return data.output;
    }

    if (data.status === "error" || data.status === "failed") {
      throw new Error(data.message || data.messege || "ModelsLab generation failed");
    }

    if (data.status !== "processing" || !data.fetch_result) {
      throw new Error(`Unexpected ModelsLab response: ${JSON.stringify(data).slice(0, 1500)}`);
    }

    if (attempt === config.max_poll_attempts) {
      throw new Error(`Timed out waiting for ModelsLab result after ${config.max_poll_attempts} polls`);
    }

    await new Promise((resolve) => setTimeout(resolve, config.poll_interval_ms));
    data = await postJson(data.fetch_result, { key: apiKey });
  }

  throw new Error("Unexpected polling termination");
}

async function downloadImage(url, basePath) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to download generated image: HTTP ${response.status}`);
  }

  const ext = extensionFromContentType(response.headers.get("content-type"), url);
  const target = `${basePath}${ext}`;
  const bytes = Buffer.from(await response.arrayBuffer());
  await fs.writeFile(target, bytes);
  return target;
}

function matchesOnly(entry, onlySet) {
  if (!onlySet) return true;
  const haystack = `${entry.heading}\n${entry.title}\n${entry.baseName}`.toLowerCase();
  return [...onlySet].some((needle) => haystack.includes(needle.toLowerCase()));
}

async function generateEntry(entry, context) {
  const { config, options, apiKey, modelId } = context;
  const basePath = path.join(config.output_dir, entry.baseName);
  const existing = await findExistingImage(basePath);

  if (existing && !options.force) {
    return { status: "skipped", entry, file: existing };
  }

  const scenePositive = stripLegacyStyle(entry.positive, config.strip_legacy_style_fragments);
  const positive = [config.common_positive, scenePositive].filter(Boolean).join(", ");
  const negative = [config.common_negative, entry.negative].filter(Boolean).join(", ");

  if (options.dryRun) {
    return { status: "dry-run", entry, positive, negative, basePath };
  }

  const payload = {
    key: apiKey,
    model_id: modelId,
    prompt: positive,
    negative_prompt: negative,
    width: config.width,
    height: config.height,
    samples: config.samples
  };

  for (const key of ["num_inference_steps", "guidance_scale", "seed"]) {
    if (config[key] !== undefined && config[key] !== null) payload[key] = config[key];
  }

  const initial = await postJson(config.endpoint, payload);
  const outputs = await waitForOutputs(initial, apiKey, config);

  const files = [];
  for (let i = 0; i < outputs.length; i += 1) {
    const suffix = outputs.length > 1 ? `_${i + 1}` : "";
    files.push(await downloadImage(outputs[i], `${basePath}${suffix}`));
  }

  const metadata = {
    heading: entry.heading,
    title: entry.title,
    date: entry.date,
    model_id: modelId,
    width: config.width,
    height: config.height,
    files,
    generated_at: new Date().toISOString(),
    prompt: positive,
    negative_prompt: negative
  };
  await fs.writeFile(`${basePath}.meta.json`, `${JSON.stringify(metadata, null, 2)}\n`, "utf8");

  return { status: "generated", entry, files };
}

async function runPool(items, concurrency, worker) {
  const results = new Array(items.length);
  let next = 0;

  async function run() {
    while (true) {
      const index = next;
      next += 1;
      if (index >= items.length) return;
      try {
        results[index] = await worker(items[index]);
      } catch (error) {
        results[index] = {
          status: "error",
          entry: items[index],
          error: error instanceof Error ? error.message : String(error)
        };
      }
    }
  }

  await Promise.all(Array.from({ length: concurrency }, () => run()));
  return results;
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const config = JSON.parse(await fs.readFile(options.config, "utf8"));
  const source = await fs.readFile(config.prompt_source, "utf8");
  const allEntries = parsePromptMarkdown(source);
  const entries = allEntries.filter((entry) => matchesOnly(entry, options.only));

  if (allEntries.length === 0) {
    throw new Error(`No illustration prompts found in ${config.prompt_source}`);
  }

  if (options.list) {
    for (const entry of entries) {
      console.log(`${entry.baseName}\t${entry.heading}`);
    }
    return;
  }

  const apiKey = process.env.MODELSLAB_API_KEY;
  if (!options.dryRun && !apiKey) {
    throw new Error("MODELSLAB_API_KEY is required. Use --dry-run to inspect without API calls.");
  }

  const modelId = process.env.MODELSLAB_MODEL_ID || config.model_id;
  await fs.mkdir(config.output_dir, { recursive: true });

  console.log(`Parsed ${allEntries.length} illustration prompts; selected ${entries.length}.`);
  console.log(`Model: ${modelId}; output: ${config.output_dir}`);

  const results = await runPool(entries, options.concurrency, (entry) =>
    generateEntry(entry, { config, options, apiKey, modelId })
  );

  let errors = 0;
  for (const result of results) {
    if (result.status === "skipped") {
      console.log(`[SKIP] ${result.entry.heading} -> ${result.file}`);
    } else if (result.status === "dry-run") {
      console.log(`[DRY]  ${result.entry.heading} -> ${result.basePath}.*`);
    } else if (result.status === "generated") {
      console.log(`[OK]   ${result.entry.heading} -> ${result.files.join(", ")}`);
    } else if (result.status === "error") {
      errors += 1;
      console.error(`[ERR]  ${result.entry.heading}: ${result.error}`);
    }
  }

  const summary = results.reduce((acc, result) => {
    acc[result.status] = (acc[result.status] || 0) + 1;
    return acc;
  }, {});
  console.log(`Summary: ${JSON.stringify(summary)}`);

  if (errors > 0) process.exitCode = 1;
}

main().catch((error) => {
  console.error(error instanceof Error ? error.stack || error.message : error);
  process.exit(1);
});
