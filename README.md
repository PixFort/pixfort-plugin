# pixfort plugin

Build and manage your pixfort WordPress website from ChatGPT, Codex, Claude Code, or Cursor. The plugin connects your AI assistant to your website and includes skills for creating pages, working with Elementor sections, and managing site layouts.

**An active [pixfort Theme subscription](https://pixfort.com/theme/) is required to use the pixfort plugin.**

## What you can do

- Create a complete website demo with coordinated pages, copy, and images.
- Edit existing Elementor content and adapt premade pixfort sections to your business.
- Find and import images and videos from the pixfort media catalog.
- Manage navigation, headers, footers, global styles, and where templates appear.
- Inspect your connected sites, content, and current website settings.

New pages are created as drafts by default. Tell your assistant when you want content published or a new layout activated on your live site.

## Before you start

You will need:

- Your pixfort account with an active pixfort Theme subscription.
- A public HTTPS WordPress site running **pixfort Theme 1.20.2 or later** and **pixfort Core 4.3.4 or later**.
- Elementor for the page-builder workflows.
- WordPress administrator access to approve the site's connection.

The plugin uses pixfort's hosted MCP server. No local server or manually supplied API key is needed. Localhost and private-network sites cannot be connected to the public service.

## Installation

Choose your client below. If pixfort is not listed in your client's marketplace yet, use the Claude Code repository installation.

### Cursor

1. Open **Customize** in the Cursor sidebar and search for **pixfort** in the [Cursor Marketplace](https://cursor.com/marketplace).
2. Select **Install** and choose whether to use it for your project or your user account.
3. Follow the pixfort sign-in prompt to authorize your account.

### Claude Code

Run these commands in your terminal:

```sh
claude plugin marketplace add PixFort/pixfort-plugin
claude plugin install pixfort@pixfort
```

Start a new Claude Code session. Open `/mcp` and complete pixfort account authorization, then run `/pixfort:connect-sites` to get started.

### ChatGPT and Codex

1. Open your client's plugin directory and search for **pixfort**.
2. Install the plugin and follow the pixfort sign-in prompt.
3. Run the `connect-sites` setup skill, or ask: “Check my connected pixfort websites and help me get started.”

## Connect your WordPress website

After authorizing your pixfort account, connect the website you want to work on:

1. Open [pixfort connected sites](https://pixfort.com/mcp-sites) and sign in to your pixfort account.
2. Choose **Connect your website** and enter your public HTTPS WordPress site URL.
3. Follow the redirect to WordPress, sign in as an administrator, and approve the **pixfort MCP** application.
4. Return to your AI assistant and ask: “List my connected websites and check whether my site is ready.”

Authorizing your pixfort account and connecting your WordPress website are separate steps. If you have multiple websites, include the site's name or domain in your request so the assistant uses the right one.

## Start using pixfort

Describe what you want to do in chat. For example:

**Create a website demo**

> Create a website demo for my architecture studio with Home, About, Projects, and Contact pages. Use a clean, editorial style and keep everything as drafts.

**Update an existing page**

> Update the introduction on my About page to describe our interior design services. Keep the existing layout and images.

**Prepare a header**

> Create a draft header with my existing logo and links to Home, About, and Contact. Keep it unpublished.

**Choose matching media**

> Find architecture photos in the pixfort catalog that match my website's colors and import the selected images into my Media Library.

**Manage navigation**

> Create a menu linking to my Home, Services, About, and Contact pages.

The plugin includes these skills, which your assistant can use as needed:

| Skill | What it helps you do |
| --- | --- |
| `connect-sites` | Connect your account and websites, select a site, and resolve connection issues. |
| `create-website-demo` | Plan and create pages with coordinated copy, Elementor sections, and media. |
| `site-layout` | Manage menus, headers, footers, global styling, and template display rules. |

## Need help?

- **No websites appear:** connect your site at [pixfort connected sites](https://pixfort.com/mcp-sites), then ask the assistant to check again.
- **Sign-in is required:** reconnect your pixfort account through your client's plugin or MCP settings.
- **Your site is incompatible:** update pixfort Theme and pixfort Core, and make sure Elementor is available for page-builder tasks.

For account, subscription, or website support, visit [pixfort support](https://pixfort.com/item-support). Learn more about the [pixfort Theme subscription](https://pixfort.com/theme/).

## License

The plugin package is available under the [MIT License](LICENSE). Access to the hosted service requires a pixfort Theme subscription and is subject to the [pixfort terms of service](https://pixfort.com/terms) and [privacy policy](https://pixfort.com/privacy-policy). pixfort trademarks, WordPress products, and catalog media retain their applicable terms.
