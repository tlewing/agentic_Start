# Chapter 8: Technology Choices

An example stack that lets you move fast without piecing things together.

---

## The Problem With Choosing Tech

When you're starting a project, you can spend weeks:
- Researching frameworks
- Comparing databases
- Setting up authentication
- Configuring deployment
- Connecting everything together

That's time not spent building your product.

---

## A Stack That Works

Here's a proven combination for mobile/web apps:

| Layer | Technology | Why |
|-------|------------|-----|
| **Frontend** | React Native + Expo | Cross-platform mobile, web capable, JavaScript ecosystem |
| **Backend** | Supabase | Auth, database, storage, realtime, edge functions — all in one |
| **Language** | TypeScript | Type safety without enterprise complexity |
| **Deployment** | Expo EAS + Vercel | Push-button deploys, no DevOps required |

This stack powers real production apps. It's optimized for speed to market with a small team (or one person with agents).

---

## Why These Choices

### React Native + Expo

**What it is:** A framework for building mobile apps with JavaScript/TypeScript. Expo adds tooling that handles the hard parts.

**Why it works:**
- One codebase for iOS, Android, and web
- Huge ecosystem of libraries
- Fast development with hot reloading
- Expo handles app store builds, updates, notifications

**The alternative:** Build separate iOS (Swift) and Android (Kotlin) apps. 2-3x the work.

### Supabase

**What it is:** An open-source Firebase alternative. Gives you a Postgres database plus auth, storage, realtime subscriptions, and edge functions.

**Why it works:**
- **Auth built-in** — Google, Apple, email/password, magic links. No Auth0 integration needed.
- **Database included** — Postgres with a nice UI. Row-level security for authorization.
- **Storage included** — File uploads handled. No S3 configuration.
- **Realtime included** — Subscriptions to database changes. No WebSocket setup.
- **Edge functions** — Serverless functions when you need custom logic.

**The alternative:** Separate services for each (Auth0 + RDS + S3 + Pusher + Lambda). More to configure, more to pay for, more to break.

### TypeScript

**What it is:** JavaScript with type checking.

**Why it works:**
- Catches errors before runtime
- Better autocomplete and refactoring
- Shared types between frontend and backend
- Works with the entire JS ecosystem

**The alternative:** Plain JavaScript. Faster to write initially, harder to maintain.

### Expo EAS + Vercel

**What it is:**
- Expo EAS (Expo Application Services) builds and submits your mobile apps
- Vercel hosts your web app and serverless functions

**Why it works:**
- Push code, get builds. No Xcode or Android Studio configuration.
- App store submission handled
- Over-the-air updates for instant fixes
- Vercel deploys on git push

**The alternative:** Manage your own CI/CD, build servers, signing certificates. Hours of DevOps.

---

## The Full Picture

```
┌─────────────────────────────────────────────────────────────┐
│                         YOUR APP                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              React Native + Expo                     │   │
│   │                                                      │   │
│   │   iOS App    Android App    Web App                  │   │
│   │      │            │            │                     │   │
│   │      └────────────┴────────────┘                     │   │
│   │                    │                                 │   │
│   └────────────────────┼─────────────────────────────────┘   │
│                        │                                     │
│                        ▼                                     │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                   Supabase                           │   │
│   │                                                      │   │
│   │   ┌──────────┐ ┌──────────┐ ┌──────────┐            │   │
│   │   │   Auth   │ │ Database │ │ Storage  │            │   │
│   │   │          │ │ Postgres │ │  Files   │            │   │
│   │   └──────────┘ └──────────┘ └──────────┘            │   │
│   │                                                      │   │
│   │   ┌──────────┐ ┌──────────┐                         │   │
│   │   │ Realtime │ │  Edge    │                         │   │
│   │   │ Subscr.  │ │ Functions│                         │   │
│   │   └──────────┘ └──────────┘                         │   │
│   │                                                      │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Getting Started With This Stack

### 1. Create Expo Project

```bash
npx create-expo-app my-app --template expo-template-blank-typescript
cd my-app
```

### 2. Set Up Supabase

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Get your project URL and anon key
4. Install the client:

```bash
npm install @supabase/supabase-js
```

5. Create `lib/supabase.ts`:

```typescript
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'YOUR_PROJECT_URL';
const supabaseAnonKey = 'YOUR_ANON_KEY';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
```

### 3. Set Up Auth

Supabase auth works out of the box:

```typescript
// Sign up
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password123',
});

// Sign in
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password123',
});

// Sign in with Google
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
});
```

### 4. Create Your Database

In Supabase dashboard, create tables. Example:

```sql
create table profiles (
  id uuid references auth.users primary key,
  name text,
  avatar_url text,
  created_at timestamp with time zone default now()
);

-- Row Level Security
alter table profiles enable row level security;

create policy "Users can read own profile"
  on profiles for select
  using (auth.uid() = id);

create policy "Users can update own profile"
  on profiles for update
  using (auth.uid() = id);
```

### 5. Query Data

```typescript
// Read
const { data, error } = await supabase
  .from('profiles')
  .select('*')
  .eq('id', userId);

// Write
const { data, error } = await supabase
  .from('profiles')
  .insert({ id: userId, name: 'John' });

// Realtime subscription
supabase
  .channel('profiles')
  .on('postgres_changes', { event: '*', schema: 'public', table: 'profiles' },
    (payload) => console.log(payload))
  .subscribe();
```

### 6. Deploy

**Mobile (Expo EAS):**
```bash
npm install -g eas-cli
eas build --platform all
eas submit --platform all
```

**Web (Vercel):**
```bash
npm install -g vercel
vercel
```

---

## Project Structure

A typical project using this stack:

```
my-app/
├── app/                    # Screens (Expo Router)
│   ├── (auth)/             # Auth screens
│   │   ├── login.tsx
│   │   └── signup.tsx
│   ├── (main)/             # Main app screens
│   │   ├── index.tsx
│   │   └── profile.tsx
│   └── _layout.tsx
│
├── components/             # Reusable UI components
│   ├── Button.tsx
│   └── Card.tsx
│
├── lib/                    # Business logic
│   ├── supabase.ts         # Supabase client
│   ├── auth.ts             # Auth helpers
│   └── types.ts            # TypeScript types
│
├── hooks/                  # React hooks
│   ├── useAuth.ts
│   └── useProfile.ts
│
├── constants/              # App constants
│   ├── colors.ts
│   └── config.ts
│
├── docs/                   # Agentic docs (copied from templates)
│   ├── _TODAY.md
│   ├── _AGENTS.md
│   └── ...
│
└── package.json
```

---

## When This Stack Fits

**Good for:**
- Mobile apps (iOS + Android)
- Web apps
- Apps with user accounts
- Apps that need realtime features
- Solo founders or small teams
- MVPs and production apps

**Consider alternatives for:**
- High-performance games (use Unity or native)
- Heavy computation (may need dedicated backend)
- Enterprise with existing infrastructure
- Apps that must be purely native

---

## Cost

For an early-stage product:

| Service | Free Tier | Paid Starts |
|---------|-----------|-------------|
| Supabase | 500MB DB, 1GB storage, 50K auth users | $25/mo |
| Expo EAS | 30 builds/mo | $99/mo |
| Vercel | 100GB bandwidth | $20/mo |

You can build and launch a real product on free tiers. Costs kick in with success.

---

## Summary

| Choice | Decision |
|--------|----------|
| **Frontend** | React Native + Expo |
| **Backend** | Supabase |
| **Language** | TypeScript |
| **Deploy** | Expo EAS + Vercel |

This stack is:
- Fast to set up
- Well-documented
- Production-ready
- Cost-effective
- Perfect for agents to work with (standard patterns, good types)

You can debate alternatives forever. Or you can use this and start building.

---

→ Back to [00_START_HERE.md](00_START_HERE.md)

