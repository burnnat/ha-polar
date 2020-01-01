## Overview
Custom component to expose data from [Polar Flow](https://flow.polar.com/) to Home Assistant. 

## Requirements

You must be registered with Polar Accesslink for API access. Login to https://admin.polaraccesslink.com/ using a Polar Flow account and create a new client application with the following information:

1. Organization Information

    - **Organization Name**: Your name or organization.
    - **Address**: Your mailing address.
    - **I intend to integrate on behalf of a client or third-party organization**: No
    - **I agree to the AccessLink Limited License Agreement**: Yes

2. Application Information

    - **Application Name**: Anything you want, must be unique.
    - **Contact Email**: Your email.
    - **Description**: Anything you want.
    - **Authorization Callback Domain**: The path `/api/polar_auth` relative to your Home Assistant instance. For example, if your Home Assistant uses the domain `homeassistant.example.com`, enter https://homeassistant.example.com/api/polar_auth

3. Available Data Types

    - **Exercise data**: Yes
    - **Daily activity data**: Yes
    - **Physical information data**: Yes

When finished, take note of the client ID and secret that were generated. You will need to include these in your configuration and will not be able to view them again later without regenerating.

## Configuration:
```
polar:
    client_id: fd1b46a2-3e59-b7f4-d85c-a4237c4fb4ad
    client_secret: acd35eb0-51e8-1c6b-7bb9-f13a1b906ae6
    unit_system: metric # Defaults to global unit_system if not specified
    monitored_resources:
        daily_activity:
            - "calories"
            - "duration"
            - "active-calories"
            - "active-steps"
        training_data:
            - "calories"
            - "club-id"
            - "club-name"
            - "detailed-sport-info"
            - "device"
            - "distance"
            - "duration"
            - "has-route"
            - "heart-rate/average"
            - "heart-rate/maximum"
            - "start-time"
            - "sport"
            - "training-load"
        physical_info:
            - "aerobic-threshold"
            - "anaerobic-threshold"
            - "height"
            - "maximum-heart-rate"
            - "resting-heart-rate"
            - "vo2-max"
            - "weight"
```
