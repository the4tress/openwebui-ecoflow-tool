# EcoFlow API Tool for Open WebUI

An Open WebUI Tool that integrates with the EcoFlow API to retrieve device information and status data. This tool enables AI assistants to help troubleshoot issues with EcoFlow devices by accessing real-time device data.

## Features

- **List All Devices**: View all EcoFlow devices registered to your account
- **Get Device Details**: Retrieve detailed status and quota information for specific devices
- **Secure Authentication**: Uses HMAC-SHA256 signature-based authentication
- **Regional Support**: Compatible with both US and EU EcoFlow API endpoints

## Prerequisites

Before using this tool, you need:

1. An EcoFlow account with registered devices
2. EcoFlow API credentials (Access Key and Secret Key)
3. Open WebUI installed and running

## Getting API Credentials

1. Visit the [EcoFlow Developer Portal](https://developer.ecoflow.com)
   - For European users: [EcoFlow Developer Portal (EU)](https://developer-eu.ecoflow.com)
2. Sign in with your EcoFlow account
3. Navigate to the API credentials section
4. Generate or copy your **Access Key** and **Secret Key**

## Installation

1. Download the [`ecoflow.py`](ecoflow.py) file
2. In Open WebUI, navigate to **Workspace** → **Tools**
3. Click **Import Tool** or **Create New Tool**
4. Upload or paste the contents of [`ecoflow.py`](ecoflow.py)
5. Save the tool

## Configuration

After installing the tool, you must configure the Valves with your API credentials:

1. In Open WebUI, go to **Workspace** → **Tools**
2. Find the **EcoFlow API Tool** and click on it
3. Click on the **Valves** or **Settings** icon
4. Configure the following values:

### Valve Settings

| Valve Name | Description | Default Value | Required |
|------------|-------------|---------------|----------|
| `ECOFLOW_API_HOST` | EcoFlow API endpoint URL | `https://api.ecoflow.com` | Yes |
| `ECOFLOW_ACCESS_KEY` | Your EcoFlow API Access Key | (empty) | Yes |
| `ECOFLOW_SECRET_KEY` | Your EcoFlow API Secret Key | (empty) | Yes |

**Important Notes:**
- For European users, change `ECOFLOW_API_HOST` to `https://api-eu.ecoflow.com`
- Keep your Secret Key confidential and never share it publicly
- Both Access Key and Secret Key are required for the tool to function

## Available Commands

### 1. List All Devices

Lists all EcoFlow devices registered to your account, including their serial numbers, names, online status, and product types.

**Function:** `list_ecoflow_devices()`

**Returns:**
- Device name and product type
- Serial number (needed for detailed queries)
- Online/Offline status

**Example Prompt:**
```
Show me all my EcoFlow devices
```

**Sample Output:**
```
Found 2 EcoFlow device(s):

• Living Room Delta (DELTA_2)
  Serial Number: R331ZEB4ZEAL0525
  Status: Online

• Garage River (RIVER_2_MAX)
  Serial Number: R351ZFB5ZBFM1234
  Status: Offline
```

### 2. Get Device Details

Retrieves detailed information and current status for a specific EcoFlow device, including battery levels, power consumption, charging status, and all available device quotas.

**Function:** `get_ecoflow_device_info(serial_number)`

**Parameters:**
- `serial_number` (required): The serial number of the device (obtain from `list_ecoflow_devices`)

**Returns:**
- Comprehensive device status data
- Battery information
- Power metrics
- All available device quotas and parameters

**Example Prompts:**
```
Get detailed information for my EcoFlow device R331ZEB4ZEAL0525
```

```
What's the current battery level and charging status of device R331ZEB4ZEAL0525?
```

```
Show me all the data for my Delta 2 with serial number R331ZEB4ZEAL0525
```

**Sample Output:**
```
Device Information for R331ZEB4ZEAL0525:

  bms_bmsStatus.maxCellTemp: 28
  bms_bmsStatus.minCellTemp: 27
  bms_bmsStatus.soc: 85
  inv_acInVol: 120
  inv_inputWatts: 450
  inv_outputWatts: 0
  pd_soc: 85
  pd_wattsInSum: 450
  pd_wattsOutSum: 0
  ...
```

## Usage Examples

### Troubleshooting with AI

Once configured, you can ask the AI assistant natural language questions about your EcoFlow devices:

**Example 1: Check device status**
```
Is my EcoFlow Delta 2 charging right now?
```

**Example 2: Battery diagnostics**
```
My EcoFlow device seems to be draining quickly. Can you check the battery status and power consumption?
```

**Example 3: Multiple device comparison**
```
Compare the battery levels of all my EcoFlow devices
```

**Example 4: Offline device troubleshooting**
```
One of my devices shows as offline. Can you help me figure out what's wrong?
```

## Troubleshooting

### "API credentials not configured" Error

**Solution:** Ensure you have set both `ECOFLOW_ACCESS_KEY` and `ECOFLOW_SECRET_KEY` in the tool's Valves settings.

### "API request failed" Error

**Possible causes:**
- Invalid API credentials
- Incorrect API host URL (check if you need the EU endpoint)
- Network connectivity issues
- EcoFlow API service downtime

**Solution:** Verify your credentials at the [EcoFlow Developer Portal](https://developer.ecoflow.com) and ensure the correct API host is configured.

### "No devices found" Message

**Possible causes:**
- No devices registered to your EcoFlow account
- API credentials belong to a different account

**Solution:** Log in to the EcoFlow mobile app to verify your devices are registered to the account associated with your API credentials.

### Device Shows as Offline

**Possible causes:**
- Device is powered off
- Device is not connected to Wi-Fi
- Device is out of range of your network

**Solution:** Check the device's physical status and network connection. The device must be online to retrieve detailed status information.

## API Documentation

For more information about the EcoFlow API:
- **US Documentation:** https://developer.ecoflow.com/us/document/
- **EU Documentation:** https://developer-eu.ecoflow.com

## Project Information

- **Author:** Ryan Fortress
- **Email:** ryan.fortress@gmail.com
- **Version:** 1.0.0
- **License:** See [LICENSE](LICENSE) file
- **Repository:** https://github.com/the4tress/openwebui-ecoflow-tool

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve this tool.

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

## Disclaimer

This tool is not officially affiliated with or endorsed by EcoFlow. Use at your own risk. Always ensure you comply with EcoFlow's API terms of service.
