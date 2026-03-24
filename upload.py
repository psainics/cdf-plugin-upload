import json, requests

### CONFIG ###
PLUGIN_NAME = "" #eg: http-plugins
PLUGIN_VERSION = "" #eg: 1.6.0-SNAPSHOT
CDAP_NAMESPACE = "" #eg: http_test
CDAP_HOST = "" #eg: cdf-euw1.datafusion-staging.googleusercontent.com
BEARER_TOKEN = "" # gcloud auth print-access-token
PLUGIN_DIR = "public"
### Do not edit below this line unless you know what you are doing. ###

plugin_config = f"{PLUGIN_DIR}/{PLUGIN_NAME}-{PLUGIN_VERSION}.json"
plugin_jar = f"{PLUGIN_DIR}/{PLUGIN_NAME}-{PLUGIN_VERSION}.jar"
plugin_config_json = None
plugin_jar_data = None

with open(plugin_jar, "rb") as jar_file:
    plugin_jar_data = jar_file.read()
with open(plugin_config, "rb") as config_file:
    plugin_config_json = json.load(config_file)

res = requests.post(
    f"https://{CDAP_HOST}/api/v3/namespaces/{CDAP_NAMESPACE}/artifacts/{PLUGIN_NAME}",
    headers = {
        "Content-Type": "application/octet-stream",
        "Artifact-Version": PLUGIN_VERSION,
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Artifact-Extends" : "/".join(plugin_config_json["parents"]),
    },
    data = plugin_jar_data,
)
if not res.ok:
    print(f"[failed to upload] response from CDAP: {res.text}")
else:
    print(f"Plugin JAR {PLUGIN_NAME} version {PLUGIN_VERSION} uploaded successfully.")
    
res = requests.put(
    f"https://{CDAP_HOST}/api/v3/namespaces/{CDAP_NAMESPACE}/artifacts/{PLUGIN_NAME}/versions/{PLUGIN_VERSION}/properties",
    headers = { "Content-Type": "application/json", "Authorization": f"Bearer {BEARER_TOKEN}" },
    data = json.dumps(plugin_config_json["properties"]),
)
if not res.ok:
    print(f"[failed to upload] response from CDAP: {res.text}")
else:
    print(f"Plugin configuration for {PLUGIN_NAME} version {PLUGIN_VERSION} uploaded successfully.")
