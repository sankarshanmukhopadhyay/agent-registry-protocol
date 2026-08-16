import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
export const repositoryRoot = path.resolve(here, "../../..");

export function readJson<T = unknown>(relativePath: string): T {
  return JSON.parse(fs.readFileSync(path.join(repositoryRoot, relativePath), "utf8")) as T;
}

export function jsonFiles(relativeDirectory: string): string[] {
  const dir = path.join(repositoryRoot, relativeDirectory);
  return fs.readdirSync(dir)
    .filter((name: string) => name.endsWith(".json"))
    .map((name: string) => path.join(relativeDirectory, name))
    .sort();
}
