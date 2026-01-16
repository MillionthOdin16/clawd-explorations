# 🦞 Clawdbot Dashboard

A beautiful, real-time web dashboard that provides complete visibility into Clawdbot's internal operations, including current state, active tasks, tool calls, message streams, and reasoning processes.

## 🚀 Features

### Core Features
- **Session Status Display**: View current session information, model, runtime environment
- **Tool Call Stream**: Real-time monitoring of all tool executions with expandable details
- **Message Stream**: Conversation history with markdown rendering
- **Reasoning Panel**: View Clawdbot's internal reasoning process
- **Task Tracker**: Track active and completed tasks with status filters
- **Dark/Light Mode**: Theme toggle for comfortable viewing
- **Auto-Refresh**: Automatic updates every 5 seconds
- **Error Handling**: Graceful error handling with retry logic
- **Responsive Design**: Works on mobile, tablet, and desktop

### New Features
- **Global Search**: Search across all data types (tool calls, messages, tasks) with real-time results
- **Data Export**: Export session data to JSON or CSV format with one click
- **Session Summary**: Visual overview showing:
  - Total tool calls with success/failure breakdown
  - Total messages count
  - Task status distribution (completed/active)
  - Session duration
- **Manual Refresh**: Refresh button to force data update
- **Search Toggle**: Collapsible search bar to save screen space

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **State Management**: Zustand
- **Data Fetching**: React Query
- **Markdown**: react-markdown
- **Theme**: next-themes

## 📋 Prerequisites

- Node.js 18+ (recommended v22)
- pnpm package manager
- Clawdbot Gateway API running and accessible

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd clawdbot-dashboard
```

### 2. Install dependencies

```bash
pnpm install
```

### 3. Configure environment

```bash
# Copy example environment file
cp .env.example .env.local

# Edit .env.local with your Gateway API configuration
# NEXT_PUBLIC_GATEWAY_API_URL=http://your-gateway-url:3000
# NEXT_PUBLIC_GATEWAY_API_KEY=your-api-key
```

### 4. Run development server

```bash
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🐳 Docker Deployment

### Build Docker image

```bash
docker build -t clawdbot-dashboard .
```

### Run with Docker

```bash
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_GATEWAY_API_URL=http://your-gateway-url:3000 \
  -e NEXT_PUBLIC_GATEWAY_API_KEY=your-api-key \
  clawdbot-dashboard
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|-----------|-------------|----------|-----------|
| `NEXT_PUBLIC_GATEWAY_API_URL` | Clawdbot Gateway API URL | `http://localhost:3000` | Yes |
| `NEXT_PUBLIC_GATEWAY_API_KEY` | API key for authentication | `""` | No |

### API Integration

The dashboard expects the Gateway API to provide the following endpoints:

- `GET /api/session/status` - Session status and runtime info
- `GET /api/session/tools` - Tool call history
- `GET /api/session/messages` - Message history
- `GET /api/session/tasks` - Task list

**Note**: Currently using mock data. Update `lib/apiClient.ts` to use real Gateway API endpoints.

## 🏗️ Deployment

### Coolify Deployment

1. Create a new application in Coolify
2. Configure:
   - **Dockerfile**: Use the provided Dockerfile
   - **Environment Variables**: Set Gateway URL and API key
   - **Port**: 3000
3. Deploy

### Vercel Deployment

```bash
# Install Vercel CLI
pnpm add -D vercel

# Deploy
vercel
```

### Other Platforms

Any platform supporting Node.js and Docker can run this application.

## 📁 Project Structure

```
clawdbot-dashboard/
├── app/                    # Next.js app directory
│   ├── layout.tsx         # Root layout with theme provider
│   ├── page.tsx            # Main dashboard page
│   └── globals.css         # Global styles
├── components/            # React components
│   ├── ui/               # shadcn/ui components
│   ├── DashboardLayout.tsx # Main layout shell
│   ├── SessionHeader.tsx   # Session info display
│   ├── ToolCallStream.tsx  # Tool call monitoring
│   ├── MessageStream.tsx   # Message history
│   ├── ReasoningPanel.tsx  # Reasoning process view
│   └── TaskTracker.tsx     # Task status tracker
├── lib/                   # Utility libraries
│   ├── apiClient.ts       # Gateway API client
│   ├── types.ts          # TypeScript types
│   └── utils/            # Utility functions
├── public/                # Static assets
└── Dockerfile            # Docker configuration
```

## 🧪 Development

### Type checking

```bash
pnpm tsc --noEmit
```

### Linting

```bash
pnpm lint
```

### Build production version

```bash
pnpm build
```

## 🔍 Troubleshooting

### Search not working

- Check browser console for JavaScript errors
- Verify search query is properly formatted
- Ensure data is loaded before searching

### Export not downloading files

- Check browser pop-up blocker settings
- Verify browser allows downloads
- Check browser console for errors

### Dashboard not connecting to Gateway

- Check that Gateway API URL is correct in `.env.local`
- Verify Gateway is running and accessible
- Check API key if Gateway requires authentication
- Check browser console for error messages

### Styles not loading

- Ensure Tailwind CSS is properly configured
- Clear browser cache and hard refresh
- Check that `globals.css` is imported in `layout.tsx`

### Build errors

```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

### Docker build fails

- Check Docker version (v20+ recommended)
- Ensure Docker daemon is running
- Verify Dockerfile syntax
- Check for missing files referenced in COPY commands

## 📊 Performance

The dashboard implements several performance optimizations:

- **Data Pruning**: Limits to 500 tool calls, 1000 messages
- **Debouncing**: Throttles rapid updates
- **Memoization**: Prevents unnecessary re-renders
- **Retry Logic**: Exponential backoff for failed requests
- **Request Timeout**: 30-second timeout for API calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

- [Next.js](https://nextjs.org/) - React framework
- [shadcn/ui](https://ui.shadcn.com/) - UI components
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework
- [React Query](https://tanstack.com/query) - Data fetching

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Contact the Clawdbot team

---

Built with 🦞 by Clawdbot
