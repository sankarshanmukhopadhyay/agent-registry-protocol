import { ArpaClient } from "./client.js";

const pythonUrl = process.env.ARPA_PY_URL;
const typescriptUrl = process.env.ARPA_TS_URL;
if (!pythonUrl || !typescriptUrl) throw new Error("ARPA_PY_URL and ARPA_TS_URL are required");

const run = async () => {
  const py = new ArpaClient(pythonUrl); const ts = new ArpaClient(typescriptUrl);
  const pyHealth = await py.health(); const tsHealth = await ts.health();
  const pyAgents = await py.listAgents(); const tsAgents = await ts.listAgents();
  const result = {
    typescript_client_to_python: pyHealth.status === "ok" && pyAgents.items?.[0]?.authority_implication === false,
    typescript_client_to_typescript: tsHealth.status === "ok" && tsAgents.items?.[0]?.authority_implication === false
  };
  console.log(JSON.stringify(result));
  if (!Object.values(result).every(Boolean)) process.exitCode = 1;
};
await run();
