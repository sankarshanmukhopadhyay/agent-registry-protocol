import { jsonFiles, readJson } from "./repository.js";

export interface RegistryDocument {
  registry?: string;
  values?: unknown[];
  entries?: unknown[];
  [key: string]: unknown;
}

export function loadRegistries(): Map<string, RegistryDocument> {
  const result = new Map<string, RegistryDocument>();
  for (const file of jsonFiles("registries")) result.set(file, readJson<RegistryDocument>(file));
  return result;
}
