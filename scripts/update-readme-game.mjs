const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN;
const login = process.env.GITHUB_LOGIN || 'juliosuas';
const fs = await import('node:fs/promises');

if (!token) {
  console.error('Missing GITHUB_TOKEN or GH_TOKEN');
  process.exit(1);
}

const now = new Date();

const query = `
query($login: String!) {
  user(login: $login) {
    login
  }
}`;

const response = await fetch('https://api.github.com/graphql', {
  method: 'POST',
  headers: {
    authorization: `Bearer ${token}`,
    'content-type': 'application/json',
    'user-agent': 'juliosuas-readme-game',
  },
  body: JSON.stringify({
    query,
    variables: { login },
  }),
});

if (!response.ok) {
  console.error(`GitHub API failed: ${response.status} ${response.statusText}`);
  process.exit(1);
}

const payload = await response.json();

if (payload.errors) {
  console.error(JSON.stringify(payload.errors, null, 2));
  process.exit(1);
}

const mergedPrs = await searchCount(`type:pr author:${login} is:merged is:public`);
const updated = now.toISOString().replace('T', ' ').slice(0, 16) + ' UTC';

const block = `<!-- STATUS-GAME:START -->
\`\`\`text
PUBLIC RECEIPTS
MERGED PRS       ${mergedPrs}
UPSTREAMS        sentry-python / responses / mitmproxy / maigret / jc
UPDATED          ${updated}
\`\`\`
<!-- STATUS-GAME:END -->`;

const readmePath = new URL('../README.md', import.meta.url);
const readme = await fs.readFile(readmePath, 'utf8');
const marker = /<!-- STATUS-GAME:START -->[\s\S]*?<!-- STATUS-GAME:END -->/;

if (!marker.test(readme)) {
  console.error('STATUS-GAME block not found');
  process.exit(1);
}

const next = readme.replace(marker, block);

if (next === readme) {
  console.log('README status block already current.');
  process.exit(0);
}

await fs.writeFile(readmePath, next);

async function searchCount(query) {
  const url = new URL('https://api.github.com/search/issues');
  url.searchParams.set('q', query);
  url.searchParams.set('per_page', '1');

  const searchResponse = await fetch(url, {
    headers: {
      authorization: `Bearer ${token}`,
      accept: 'application/vnd.github+json',
      'user-agent': 'juliosuas-readme-game',
    },
  });

  if (!searchResponse.ok) {
    console.error(`GitHub search failed: ${searchResponse.status} ${searchResponse.statusText}`);
    process.exit(1);
  }

  const searchPayload = await searchResponse.json();
  return searchPayload.total_count;
}
