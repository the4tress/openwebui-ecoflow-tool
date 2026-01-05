"""
title: EcoFlow API Tool
author: Ryan Fortress <ryan.fortress@gmail.com>
project_url: https://github.com/the4tress/openwebui-ecoflow-tool
open-webui-url: https://openwebui.com/posts/d821fcde-bd0a-4ab0-9985-13f8238dd376
version: 1.0.0
about:
  This is a Tool for Open WebUI to get Ecoflow device information from the Ecoflow API (https://developer.ecoflow.com/us/document/)
  There are two commands: [List all devices, Get device details]
  Use https://api-eu.ecoflow.com for European access (docs at https://developer-eu.ecoflow.com).
"""

import requests
import hmac
import hashlib
import json
import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class Tools:
    class Valves(BaseModel):
        ECOFLOW_API_HOST: str = Field(
            default="https://api.ecoflow.com",
            description="EcoFlow API Host URL (default: https://api.ecoflow.com)",
        )
        ECOFLOW_ACCESS_KEY: str = Field(
            default="",
            description="EcoFlow API Access Key from https://developer.ecoflow.com",
        )
        ECOFLOW_SECRET_KEY: str = Field(
            default="",
            description="EcoFlow API Secret Key from https://developer.ecoflow.com",
        )

    def __init__(self):
        self.valves = self.Valves()

    @property
    def access_key(self):
        return self.valves.ECOFLOW_ACCESS_KEY

    @property
    def secret_key(self):
        return self.valves.ECOFLOW_SECRET_KEY

    @property
    def api_host(self):
        return self.valves.ECOFLOW_API_HOST

    def _flatten_object(self, obj, parent_key=""):
        """
        Flatten a nested dictionary for signature generation.
        """
        flattened = {}

        for key, value in obj.items():
            prop_name = f"{parent_key}.{key}" if parent_key else key

            if isinstance(value, dict):
                flattened.update(self._flatten_object(value, prop_name))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        flattened.update(
                            self._flatten_object(item, f"{prop_name}[{i}]")
                        )
                    else:
                        flattened[f"{prop_name}[{i}]"] = item
            else:
                flattened[prop_name] = value

        return flattened

    def _build_data_string(self, data):
        """
        Build the data string for signature generation.
        """
        if not data:
            return ""

        flattened = self._flatten_object(data)
        sorted_keys = sorted(flattened.keys())
        parts = [f"{key}={flattened[key]}" for key in sorted_keys]
        return "&".join(parts)

    def _create_signature(self, payload=None):
        """
        Create HMAC-SHA256 signature for EcoFlow API authentication.
        """
        timestamp = str(int(datetime.now().timestamp() * 1000))
        nonce = str(uuid.uuid4())

        # Build the data string
        data_string = self._build_data_string(payload or {})

        # Append access key, nonce, and timestamp
        if data_string:
            sign_string = f"{data_string}&accessKey={self.access_key}&nonce={nonce}&timestamp={timestamp}"
        else:
            sign_string = (
                f"accessKey={self.access_key}&nonce={nonce}&timestamp={timestamp}"
            )

        # Create HMAC-SHA256 signature
        signature = hmac.new(
            self.secret_key.encode("utf-8"), sign_string.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        return {
            "accessKey": self.access_key,
            "timestamp": timestamp,
            "nonce": nonce,
            "sign": signature,
        }

    def _make_request(self, method, url, payload=None):
        """
        Make an authenticated request to the EcoFlow API.
        """
        if not self.access_key or not self.secret_key:
            return {
                "error": "EcoFlow API credentials not configured. Please set ECOFLOW_ACCESS_KEY and ECOFLOW_SECRET_KEY in the tool's Valves settings."
            }

        # Create signature
        auth_params = self._create_signature(payload)

        # Prepare headers
        headers = {
            "accessKey": auth_params["accessKey"],
            "timestamp": auth_params["timestamp"],
            "nonce": auth_params["nonce"],
            "sign": auth_params["sign"],
            "Content-Type": "application/json;charset=UTF-8",
        }

        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=payload)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=payload)
            else:
                return {"error": f"Unsupported HTTP method: {method}"}

            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}

    def list_ecoflow_devices(self) -> str:
        """
        List all EcoFlow devices registered to your account.
        Returns device information including serial number, device name, online status, and product name.
        """
        url = f"{self.api_host}/iot-open/sign/device/list"
        result = self._make_request("GET", url)

        if "error" in result:
            return result["error"]

        # Format the response
        if "data" in result and isinstance(result["data"], list):
            devices = result["data"]
            if not devices:
                return "No devices found in your EcoFlow account."

            output = f"Found {len(devices)} EcoFlow device(s):\n\n"
            for device in devices:
                sn = device.get("sn", "N/A")
                name = device.get("deviceName", "N/A")
                online = "Online" if device.get("online") == 1 else "Offline"
                product = device.get("productName", "N/A")
                output += f"• {name} ({product})\n"
                output += f"  Serial Number: {sn}\n"
                output += f"  Status: {online}\n\n"
            return output
        else:
            return f"Unexpected response format: {json.dumps(result, indent=2)}"

    def get_ecoflow_device_info(
        self,
        serial_number: str = Field(
            ..., description="The serial number of the EcoFlow device to query."
        ),
    ) -> str:
        """
        Get detailed information and current status for a specific EcoFlow device.
        Requires the device serial number (can be obtained from list_ecoflow_devices).
        """
        if not serial_number:
            return "Error: Serial number is required. Use list_ecoflow_devices to get device serial numbers."

        url = f"{self.api_host}/iot-open/sign/device/quota/all?sn={serial_number}"
        result = self._make_request("GET", url)

        if "error" in result:
            return result["error"]

        # Format the response
        if "data" in result:
            data = result["data"]
            if not data:
                return f"No data available for device {serial_number}. The device may be offline or not supported."

            output = f"Device Information for {serial_number}:\n\n"

            # Pretty print the data
            for key, value in sorted(data.items()):
                output += f"  {key}: {value}\n"

            return output
        else:
            return f"Unexpected response format: {json.dumps(result, indent=2)}"
