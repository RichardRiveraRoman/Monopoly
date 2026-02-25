# Monopoly

Current structure does not reflect this layout it will be sometime to migrate towards as the application scales.

```text
Monopoly/
├── apps/
│ ├── web/ # React frontend
│ └── api/ # Python backend
├── packages/
│ ├── ui/ # Reusable React components
│ └── utils/ # Shared utility functions
├── tools/ # Scripts for builds/testing
├── configs/ # ESLint, Jest, etc.
└── package.json # Root workspace config
```
