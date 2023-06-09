# Programming JS Onboard Misty

Misty’s onboard [JavaScript API](https://github.com/MistyCommunity/Documentation/blob/master/src/content/misty-i/coding-misty/local-skill-architecture.md) allows Misty to store and run skills internally. For each skill, Misty requires the JavaScript code and the associated JSON file.

### JSON File

[JSON](https://en.wikipedia.org/wiki/JSON) (JavaScript Object Notation) files are human-readable representations of objects that can be generated and interpreted by many programming languages. In order for JavaScript code to run properly on Misty, you also need to provide a JSON metadata file like the one below.

```json
{
    "Name": "Skill name",
    "UniqueId": "an ID generated in Misty Studio",
    "Description": "Skill description",
    "StartupRules": [
        "Manual",
        "Robot"
    ],
    "Language": "javascript",
    "BroadcastMode": "verbose",
    "TimeoutInSeconds": 600,
    "CleanupOnCancel": false,
    "WriteToLog": false,
    "Parameters": {
        "Int": 10,
        "String": "twenty"
    }
}
```

The name of the JSON file must match the name of the JS file in order for it to be recognized correctly. Example: [changeLED.js](https://github.com/SWorster/MistySURF2023/blob/27a8c79d4c6ebf93c16c81fe7a837851831908e1/Onboard%20JS/changeLED.js) and [changeLED.json](https://github.com/SWorster/MistySURF2023/blob/27a8c79d4c6ebf93c16c81fe7a837851831908e1/Onboard%20JS/changeLED.json).

- The `Name` is what we refer to the skill as. This should be the same as the file name.
- The `UniqueId` is a globally unique ID (GUID) that Misty will use to identify the skill
- `StartupRules` is an array of strings that defines when and how the skill would start. If `"Manual"` is used, then the user is able to control when the skill is active or not. If `"Startup"` is used, the skill is activated upon Misty being started.
- `BroadcastMode` controls `SkillData` messages and has 3 options
  - `off` will cause the skill not to send any `SkillData` messages
  - `debug` will cause the skill to send error and debug messages to `SkillData` events
  - `verbose` does the same as debug but also sends a message to `SkillData` events for each command that Misty gets
- `TimeoutInSeconds` is the duration that the skill runs for before it cancels its execution, _in milliseconds._
- `CleanupOnCancel` is a boolean that determines whether processes in progress should stop when the skill ends.
- `WriteToLog` is a boolean used to specify whether the data from debug messages are also written to an internal log file in Misty.
- The `Parameters` will be usable through the global `_params` variable. 

In order to get a `UniqueId`, go to the Skill Management subtab under Programming in Misty Studio. There, you can generate a new JSON file with a name of your choosing to use with your new JS skill file. This is also where you can upload your JS and JSON file at the same time in order to create a new skill.

### JS File

In order to get started, make sure that you have the Misty JavaScript extension installed on VSCode, or peruse the examples found here. The documentation for the Web API is also very useful since most of the methods can be used onboard as well.
