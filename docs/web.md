# The web interface

`llossless serve` runs LLossless as a web page on your own machine: add documents, pick a model, watch the run, read the result. It runs the same merge and the same checks as `llossless merge`. This page explains how to start the server, set up accounts and keys, choose a model and run a merge, and what the server keeps and for how long, and ends with the JSON API and the security details. The [README](../README.md) has the short version, the [command-line reference](reference.md) explains the settings both interfaces share, and [Reading the report](report.md) explains the findings.

![The web interface after a run with findings. The answers came from a scripted test endpoint, not a real model.](img/web-ui-light.png)

*A finished run with findings. The answers in this screenshot came from a scripted test endpoint, not from a real model.*

**In short**

- The server answers on this machine only, at `http://127.0.0.1:8765`, until you start it with `--host`.
- The first start prints a one-time address that creates the first account. There is no default password.
- Every account can hold its own API keys. A member who has none runs on the operator's key, so give an account only to people you trust with that key.
- Only the person who submitted a run can see it.
- Documents and results are deleted 48 hours after a run finishes, unless you set `--retention`.

**On this page**

- [Quick start](#quick-start)
- [Starting the server](#starting-the-server)
- [Accounts](#accounts), [whose key a run uses](#whose-key-a-run-uses), [who can see a run](#who-can-see-a-run)
- [API keys and endpoints](#api-keys-and-endpoints)
- [Choosing a model](#choosing-a-model)
- [Subscription routes](#subscription-routes)
- [Running a merge](#running-a-merge)
- [Retention](#retention)
- [Languages](#languages)
- [What a request may choose](#what-a-request-may-choose)
- [The JSON API](#the-json-api)
- [Security details](#security-details)
- [For contributors](#for-contributors)

## Quick start

1. Start the server. From a cloned repository without installing, use `PYTHONPATH=src python3 -m llossless serve` instead.

   ```sh
   llossless serve
   ```

2. The terminal prints a one-time address that ends in `#setup=` and a long code. Open it in a browser on the same machine, choose a username and a password of at least 10 characters, and press **Create the account**. This first account is the operator's.
3. Press **Credentials** at the top right and give the server a model to use. Do one of these, then press **Done**:
   - paste an API key for Anthropic, OpenAI or Google and press **Save**;
   - enter the address of your own model server under `self-hosted` and press **Save endpoint**;
   - tick **Answer merges with this tool** beside a Claude Code row, if the server found the `claude` program.
4. In step 1, **Documents**, paste or upload at least two documents. In step 2, **Model**, pick a row.
5. Press **Merge and check**. The button names how the run is paid for, for example `Merge and check - metered API`.
6. The right-hand pane shows the progress and then the result: a verdict, the merged document and the findings.

## Starting the server

`llossless serve` takes five flags:

| flag | default | what it does |
|---|---|---|
| `--port PORT` | `8765` | The port to listen on. `0` picks a free port and prints it. |
| `--host HOST` | `127.0.0.1` | The address to listen on. Any address other than this machine's own needs an account or an access token: see [Opening the server to a network](#opening-the-server-to-a-network). |
| `--work-dir DIR` | a `web` folder in the cache directory | Where submitted documents and their results are kept until they are deleted. Only its owner can read it. |
| `--workers N` | `1` | How many merges run at the same time. Further runs wait in a queue. Raise it only if your model endpoint can serve that many runs at once. |
| `--retention SECONDS` | `172800` (48 hours) | How long a finished run is kept. `0` keeps runs until someone deletes them. See [Retention](#retention). |

It reads five environment variables of its own:

| variable | what it does |
|---|---|
| `LLOSSLESS_RETENTION` | The same as `--retention`, for a server started without a command line. The flag wins. A value that is not a number stops the server from starting. |
| `LLOSSLESS_WEB_TOKEN` | An access token of at least 16 ASCII characters, for a network address while the server has no account yet. |
| `LLOSSLESS_ACCOUNTS` | Where the accounts file is. Default: `~/.config/llossless/accounts.json`. |
| `LLOSSLESS_CREDENTIALS` | Where the operator's shared keys and endpoints are stored. Default: `~/.config/llossless/credentials.json`. |
| `LLOSSLESS_COMMANDS` | Where the [subscription routes](#subscription-routes) are stored. Default: `~/.config/llossless/commands.json`. |

The cache directory is `.llossless-cache/` in a cloned repository and `~/.cache/llossless` for an installed package. `XDG_CACHE_HOME` and `XDG_CONFIG_HOME` replace `~/.cache` and `~/.config` where they are set.

The server also reads the variables the command line reads, such as `LLOSSLESS_BASE_URL`. They define "this server's own endpoint", which is where a [typed model id](#a-model-that-is-not-in-the-table) goes by default.

Stop the server with Ctrl+C. That signs everybody out. Runs are kept: see [After a restart](#after-a-restart).

### Opening the server to a network

By default only this machine can reach the server. With `--host` and another address, anyone who can reach that address can reach the server, so every request must then be signed in. The simplest order is:

```sh
llossless serve                  # once: open the printed address, create the first account, stop with Ctrl+C
llossless serve --host 0.0.0.0   # from now on: reachable from the network, sign-in required
```

A server with no account refuses to start on a network address, unless `LLOSSLESS_WEB_TOKEN` is set. With the token, the first account can be created over the network. Open the address the server prints, with the server's name or address as the host. The page asks for the access token first: type the value of `LLOSSLESS_WEB_TOKEN`. The form that creates the first account appears next. The page keeps the token only while it is open, and stops sending it once the account exists. A script has to send the token itself, in an `X-LLossless-Token` header on every API request, until the first account exists. Once an account exists, the token is no longer used.

The server speaks plain HTTP. For anything beyond a trusted network, put a reverse proxy with TLS in front of it. The proxy must pass the `Host` header through and send `X-Forwarded-Proto: https`. The server then marks the sign-in cookie `Secure` and accepts the page's requests. Without that header, every request that changes something, sign-in included, is refused with 403 `cross_origin`.

## Accounts

### The first account

A new server has no accounts and answers nothing except the form that creates the first one. Every start prints a one-time address for that form. The address works once, only while there is no account, and is different on every start. There is no default password.

The first account is the **operator**: the person who runs the server. Keys and endpoints that are already stored on the server become the operator's, and they are the ones every later account shares.

### Operators and members

Every other account is a **member**.

| | operator | member |
|---|---|---|
| Run merges, and see, cancel and retry their own runs | yes | yes |
| Set endpoints and keys | the shared ones, used by everybody | their own, used only by their runs |
| Change their own password | yes | yes |
| Add and remove accounts | yes | no |
| Switch subscription tools on and off | yes | no |
| Cancel somebody else's run | yes | no |
| See somebody else's run | no | no |

The operator adds an account in **Credentials**, under **Accounts**: a username, a password, **Add**. A username is 2 to 32 characters: lowercase letters, digits, dot, dash or underscore. A password is at least 10 characters.

Removing an account deletes the keys and the saved settings it had stored, signs it out, and cancels its queued and running runs. Its finished runs stay on the server, visible to nobody, until [retention](#retention) deletes them. The last operator account cannot be removed.

Anyone can change their own password under **Your password**, which signs that account out everywhere. Setting somebody else's password and adding a second operator work only through the [API](#the-json-api).

If the only operator's password is lost, the page offers no recovery. Stop the server, delete the accounts file and the `users` folder beside the credentials file, and start again. The server is then back in setup: every account is gone, and the shared keys become the new first account's.

A sign-in ends after 12 hours without use, and after 7 days in any case. Restarting the server signs everybody out.

### Before you give someone an account

**They can spend your money.** A member who has not set up their own endpoint for a provider runs on the operator's endpoint, with the operator's key, and so on the operator's credit. There is no spending limit per account. Anyone who can sign in can therefore spend as much as the operator's key allows. Only give an account to someone you would trust with that key.

**They can make the server send requests.** A member can save an endpoint address of their own, and the server then sends model requests to it. That address can be anything the server can reach, including a machine on its own network that the member cannot reach directly.

### Whose key a run uses

**A run uses the key of the person who submitted it.** If two people run at the same time, each run spends its own submitter's key, and neither can see the other's.

There are two kinds of endpoint:

- **The operator's.** Set up once and shared with every account. Only the operator can change it.
- **Your own.** Private to your account. For your runs it replaces the operator's endpoint for that provider, and it uses your key.

So a member with no endpoint of their own for a provider runs on the operator's, and a member who has one runs on theirs. A key can only be stored together with an endpoint address of your own. The reason: a key saved without an address would be sent to whichever address happens to be in effect, which may not be one you chose.

### Who can see a run

**Only the person who submitted a run can see it.** That covers the list of runs, a run's status, its report, the merged document, the live progress stream and deleting it. A request for somebody else's run gets exactly the answer a run that does not exist gets. Knowing a run's id is not enough to open it: an id shows up in the address bar, in browser history and in links pasted into a chat, so it is not treated as a secret.

The one exception is cancelling: an operator may cancel anybody's run, because it may be spending the operator's key.

## API keys and endpoints

**Credentials** lists four providers: `anthropic`, `google`, `openai` and `self-hosted`. Each has an endpoint, which is the address requests are sent to, and an API key. A model can be picked only when its provider has an endpoint.

- **Anthropic, OpenAI, Google.** The usual address is already shown (`https://api.anthropic.com/v1`, `https://api.openai.com/v1`, `https://generativelanguage.googleapis.com/v1beta/openai`). Paste the key and press **Save**: the address is stored with it. **Change address** opens the field, for a proxy or a regional endpoint.
- **Self-hosted.** Enter the address of your own OpenAI-compatible server, for example `http://localhost:11434/v1` for Ollama, and press **Save endpoint**. A key is optional.

When an endpoint is saved, the server asks it which models it serves, without sending a key, and the models it lists appear in the picker. An endpoint that does not answer can still be used: type the model id, as described under [A model that is not in the table](#a-model-that-is-not-in-the-table).

What to know:

- **Each row saves on its own button.** **Done** only closes the sheet. Text that was typed and not saved is dropped.
- **A key is never shown again.** The sheet shows whether a key is set. The last four characters are shown only to the account the key belongs to: the operator for a shared key, a member for a key of their own. A member's row for a shared key reads **set by the operator**.
- **Saving an endpoint clears the key stored for that provider.** A key is only ever sent to the address it was saved with, so after changing an address, paste the key again. A run that is under way when its endpoint's address is changed gets no key for that provider from then on and fails on its next call: retry it once the new key is saved. The same holds when the operator deletes a shared key: no run under way sends it again, a member's included.
- **A key saved with a `self-hosted` address is sent to that address only.** `self-hosted` and this server's own endpoint read the same variable, `LLOSSLESS_API_KEY`. So once a key is saved with a self-hosted address, a typed model id that goes to this server's own endpoint is sent without a key, unless the two addresses are the same.
- **Some addresses are refused:** one that is not `http://` or `https://`, one with a username or password in it, one with a `?` or a `#` in it, and a plain `http://` address on another machine while a key that would be sent to it is set, because the key would travel unencrypted. For a member that means a key of their own: the operator's shared key is never sent to a member's address and does not count.
- **A member's own rows.** A member can set an endpoint and a key of their own for any provider, including one the operator shares. For a shared provider the row reads **set by the operator** and its fields start empty: the operator's address and key are never filled in. Once the member saves an endpoint of their own, the row reads **yours** and their runs use it. A member sees an operator's endpoint as scheme, host and port only, never its path.
- **A key given as an environment variable has no address stored with it.** It is sent to whichever address is in effect for its provider, also after that address is changed on the page. To move such a provider, change both variables where the server is started, or save the key on the page together with the new address.
- **Where it is stored.** The operator's keys and endpoints are in the shared credentials file, and every other account has a file of its own in a `users` folder beside it. The operator can also provide them as environment variables when starting the server: each row names its two variables.

## Choosing a model

Step 2, **Model**, lists only what you can run right now: models LLossless has measured whose provider has an endpoint, models an endpoint listed when it was saved, and [subscription routes](#subscription-routes) that are switched on. With nothing set up, the step says so and offers the **Credentials** button.

### The picker

Each row is one way to reach a model. The same model can appear twice, once through an API and once through a subscription. The badge after the name tells the two apart:

| badge | colour | what it means |
|---|---|---|
| metered API | amber | A vendor's API. Every call is billed to the key in use. |
| subscription | blue | A program on the server that runs on a flat-rate plan. The run counts against that plan. |
| command on this server | blue | A hand-written route that is not marked as a subscription. |
| local | grey | A self-hosted endpoint. |
| route not identified | grey, dashed | The page cannot tell where the run would go. |

The **Merge and check** button repeats the badge of the selected row. A subscription route that is switched on is preselected ahead of the metered rows.

The four figure columns come from LLossless's own test runs, which [the results page](results.md) explains. **Cost** is what one merge cost at list prices, and **Speed** is how many seconds it took. **Loss** counts the facts that went missing without the merge saying so, and **Deviations** counts the changes it made without flagging them, both per test. Lower is better in all four.

Each figure is shown as a band, in a word and a colour: **excellent**, **good**, **fair** or **poor**. Cost also shows the price. A cell with no figure says why: **on plan** (a subscription has no price per merge), **per GPU-minute** (a self-hosted model is billed by time), **free tier** (measured on a vendor's free quota) or **unmeasured** (nobody has run this model through LLossless). A model that an endpoint listed is always unmeasured.

Click a column heading to sort by it, and again to reverse. Rows without a figure sort last either way. Sorting never changes the selection.

### The scorecard

**Model scorecard** opens every measured model and route, including those you cannot run here. It shows the numbers behind the bands, how many tests each was measured over, and the date. A row you cannot run says why, for example `no endpoint configured for anthropic`. **About this list** at the bottom states where each band begins and what every marker means.

### A model that is not in the table

Tick **Use a model id not in the table**. Three fields appear:

- **Model id.** It is sent exactly as typed. LLossless never guesses a provider from a name.
- **Send it to.** This server's own endpoint, or one of the endpoints set up under Credentials. An id the table already knows goes to that row's endpoint instead, and the page says so. A member who has a `self-hosted` endpoint of their own and sends an id to this server's own endpoint sends it without a key.
- **Context window (tokens).** The number of tokens the model accepts, from 4,096 to 10,000,000. It is required when the id goes to Anthropic, OpenAI or Google, because those endpoints do not report it and LLossless does not guess it. The figure is on the vendor's page for the model. It is optional for this server's own endpoint and for a self-hosted one: left empty, the window is measured, which works on an Ollama server.

The context window field also appears when you pick a row that an endpoint listed and LLossless has no window for.

### A different model for the checks

Normally one model writes the merge and runs the checks. Tick **Use a different model for the checks** and a **Check** column appears, so the two can be chosen separately. The report names both. When the two are paid for differently, the button names both, for example `Merge - metered API, check - local`.

This is not available with a subscription route: that program does the merge and the checks itself. A subscription row also cannot do only the checks.

## Subscription routes

A subscription route answers a run by starting a program on the server, such as the Claude Code CLI on a flat-rate plan, in place of a metered API.

**A browser never names the program.** A request carries only the id of a route. The command comes from a file on the server that only the operator can write. A form that accepted a command would let anyone who can sign in run any program on the server.

### Switching one on from the page

**Credentials** has a section **Subscription tools on this server**. The server looks for the tools it knows by name: first on its own `PATH`, then in `~/.local/bin`, `/usr/local/bin`, `~/.npm-global/bin` and `/opt/homebrew/bin`. This version knows one tool, `claude` (Claude Code), and offers one row per model: Haiku, Sonnet, Opus and Fable. Each row says **found** or **not found**. The page never shows where the program is.

Tick **Answer merges with this tool** to add the row to the picker. Only the operator can do this, because a route is shared by every account. On an untouched page the Opus row is preselected, or a route you wrote by hand if there is one. Fable, the most expensive, is never preselected.

### Writing a route by hand

For another program, another model or other arguments, the operator writes the route into the commands file:

```json
{
  "version": 1,
  "routes": {
    "opus-sub": {
      "label": "Opus - Subscription",
      "command": "claude --print --output-format json --model opus",
      "window": 200000,
      "model": "opus",
      "envelope": "result",
      "web_tools": []
    }
  }
}
```

The key (`opus-sub` here) is the route's id: lowercase letters, digits, hyphen and underscore, at most 64 characters.

| field | required | meaning |
|---|---|---|
| `label` | yes | The name shown in the picker, exactly as written. |
| `command` | yes | The program and its arguments. It gets the prompt on standard input and writes the answer to standard output. It is never sent to a browser. |
| `window` | yes | The model's context window in tokens. A program cannot be asked for it. |
| `model` | yes | The model the command selects. The report records this name. Nothing checks that the command really selects it, so make sure it does. |
| `envelope` | no, `raw` | How the program answers. `raw`: its output is the answer. `result`: its output is a JSON result envelope, which is what `--output-format json` produces. The field and the command must agree. |
| `web_tools` | no, none | The web tools the command's own `--allowed-tools` grants: `WebSearch`, `WebFetch` or both. Listing a tool the command does not grant is refused. |
| `timeout` | no, `890` | Seconds one call may take. State it for a slower program. |
| `profile` | no, `subscription` | Leave it out for a flat-rate plan. With another profile the row's badge reads "command on this server". |

A row with a missing or unknown field is refused, and only that row: the Credentials sheet and the terminal name it and the reason, and every other route still works. The file must be readable and writable by its owner only, or none of its routes is offered. With no file, the server offers no subscription route.

The page marks the rows it wrote with `"discovered": true`. It switches only those on and off, and never changes a row written by hand.

### What a subscription row tells you

| note | what it means |
|---|---|
| on plan | The run counts against a subscription. LLossless cannot see how much of it a merge uses. This does not mean free. |
| shared | The program runs under the server's own login. Every account on this server uses the same subscription and the same rate limit. |
| not directly comparable | Nothing enforces the answer format and the randomness cannot be fixed, so two runs can differ. Compare its figures with other subscription rows, not with API rows. |
| retrieval (WebSearch, WebFetch) | At the `sourced` fidelity level, the model may search the web. A search can send text from your documents to a third party. |
| needs Claude Code ... or newer | The `claude` program on the server is too old for this model, and the run will be refused. Claude Opus 5.5 needs Claude Code 2.1.280 or newer. |

The report of such a run says the content left this machine. LLossless cannot see what the program sends, so it does not claim that nothing left.

### Safe mode for `claude`

A route whose program is `claude` runs in the CLI's safe mode. Your personal `CLAUDE.md`, skills, plugins and MCP servers are not loaded. The model gets no tools, except the two web tools at the `sourced` fidelity level. To do this, the server adds `--safe-mode` and `--tools` to the command.

A `--safe-mode` or `--tools` in your own command is kept as you wrote it. A grant in your own `--allowed-tools` applies at every fidelity level. A `sourced` run is refused on a route that cannot use a web tool. To run the CLI with your own setup, wrap it in a script with a different name: a wrapper is started exactly as written.

### Merge effort

When the selected route's program accepts an effort level, step 3 shows a **Merge effort** slider: low, medium, high, extra high, max. It starts at high for Opus and at medium for the other models. Haiku has a single level, so it gets a line saying so and no slider. A route written by hand gets the slider when its program is `claude` and its command names no `--effort` of its own.

The level applies to writing the merge. The checks run at low. The report records the level you chose.

The **?** beside the slider shows what LLossless measured at the selected level: how many planted errors the merge fixed in the test documents, the time per merge, and how often the model searched the web. A level nobody measured says so. The figures come from a few runs on small test documents and are a guide, not a promise. [For contributors](#for-contributors) says where the runs are.

Two warnings stay visible:

- At **max**, a warning under the slider and above the **Merge and check** button says the run may use a large share of the subscription's weekly allowance. In the one test where max was measured, it fixed no more errors than extra high and took about twice the time and usage.
- At **low** together with the `sourced` fidelity level, a note says the combination is not recommended.

## Running a merge

The left pane holds four steps and the run bar. The right pane shows the current run or the list of previous runs. A **?** beside a control explains it.

### The four steps

**Step 1, Documents.** Paste each document into its own tab, press **Upload files**, or drop files onto the document. A merge takes 2 to 12 documents.

- Several files uploaded or dropped at once become one document each, in the order given.
- Text you already typed is never overwritten: files go into empty tabs.
- A file that is not text, a file that is too large, or a file past the twelfth is not loaded, and the page names it. One submission may hold about 4 MB in total.
- **Name** is what the report calls the document. **Base document** decides whose structure the merged document follows. It starts as the first document.

**Step 2, Model.** See [Choosing a model](#choosing-a-model).

**Step 3, Settings.**

- **How much the wording may change** is the fidelity level, from `verbatim` (only your own sentences, copied exactly) to `sourced` (the model may correct facts and look them up on the web). It starts at `high`. **See examples** shows what each level does to one small text.
- **How thoroughly to check**. **Full** checks that nothing was lost and nothing was invented. **Coverage** checks only that nothing was lost. Each option shows how many model calls it needs for the documents you loaded.
- **Merge effort** appears on a subscription route only: see [Merge effort](#merge-effort).

**Step 4, Tuning.**

- **How much may be left out** is the share of your documents the merge may openly leave out. It starts at 0.03, which is 3%. A merge that goes over it is still delivered, marked for review.
- **Title** decides where the merged document's title comes from: `keep-base`, `choose-best` or `synthesise`. It starts at `synthesise`.

The [command-line reference](reference.md) explains these settings in full. They are the same as `--fidelity`, `--verify-depth`, `--loss-budget` and `--title-policy`.

### Starting the run

The status line under the button says **more input needed** in amber, with what is missing, or **ready** in green. The button works only when it says ready. **Merge and check** sends the documents. From then on the run belongs to the server: you can close the tab and come back later.

**Start over** clears the documents, the settings and the result from the page, after asking. The run itself stays in **Previous runs**.

### Saved defaults

Tick **Save these settings as my defaults** before you start a run. When the run is accepted, the server stores your choices for your account: the models, the context window, the merge effort and the settings of steps 3 and 4. Documents are never stored this way. From then on the page starts from these choices, in every browser you sign in from.

**Reset to server defaults**, in step 4, removes them again, after asking. If a saved choice is no longer available, for example a model whose endpoint was removed, the page says which one, uses the server's default for it, and offers **Update my defaults**.

### While it runs

- **Current run** shows the progress log, step by step, with the model, the endpoint and the settings the run is using.
- **Stop watching** stops the page following the run. The run goes on.
- **Cancel run** asks first, then stops the run. No further model call is made, and a subscription program is stopped. Calls already made are billed, and a call that was cut off may still be billed. A run cancelled while it was running keeps a report of what ran.
- **Notify me** asks the browser for permission, then shows a notification when the run ends. It says "Run finished" or "Run failed" and the run's short id, and nothing from your documents.
- **Run this from the command line** shows the `llossless merge` command that matches this run, with a **Copy command** button and the file name to save each document under. Your key is never in it. For a subscription route the program is not in it either. For a member, an endpoint the operator set up is named by scheme, host and port only, and a note says so.

### The result

- **The verdict**: "Passed every check", "Needs your review", "Document passed, notes are off" or "Not cleared", with a sentence on what to do.
- **Merged document**, with five buttons: **Copy merged document**, **Download markdown**, **View report** (the full report in a new tab), **Download report** (the same report as one HTML file) and **Download everything** (a zip with your documents, the merged document, `report.json` and `report.html`). A sentence below them says how long the run is kept.
- **Findings**, in tabs. **What needs your attention** lists every item that needs a decision from you and says what to decide. **Conflicts** and **Omitted content** hold the findings by kind. **Attributions**, **Number format** and **Added from outside your documents** appear only when they have something. **Claims** lists every checked claim. **What was checked** lists each check and whether it ran, then the run's details: models, route, settings, calls, tokens and cost.

A finding names its **Source**, the **Evidence**, the document it was **Checked against** and **Why it was flagged (the checker's words)**. [Reading the report](report.md) explains each kind of finding.

Over plain `http://` to an address other than localhost, a browser does not let a page write to the clipboard. **Copy merged document** then selects the text so you can copy it yourself.

### Previous runs and the queue

**Previous runs** lists your runs, newest first. What it offers depends on the run's state:

| state | what the list offers |
|---|---|
| queued | Its place in the queue, for example "position 2 of 3", and **Follow**. |
| running | **Follow**, which shows its progress under **Current run**. |
| done | **Open**, which shows its HTML report in a new tab, and three downloads: **Download markdown** (the merged document), **Download report** and **Download everything**. |
| cancelled | **Open**, **Download report** and **Download everything**: what ran before the cancel. The merged document may not exist. |
| failed | The reason, **Show log** and **Retry**. |
| interrupted | **Show log** and **Retry**. See [After a restart](#after-a-restart). |

All accounts share one queue, and `--workers` sets how many runs it serves at once. The list updates by itself while a run is queued or running.

**Retry** starts a new run from the same documents and settings, after asking. Every model call is made again and may be billed again. Only the run's submitter can retry it, and only while its documents are still on the server.

The downloads work until the run is deleted. The [API](#the-json-api) serves the same files.

### After a restart

- **Queued runs** keep their place and start when their turn comes. Finished runs are listed again.
- **A run that was running** when the server stopped is marked **interrupted**. It is never restarted by itself, because that would make and bill its model calls again. **Show log** shows what it had done, and **Retry** starts it again as a new run.
- **Runs whose retention period ended** while the server was down are deleted before anything is served.

For operators: the work directory holds one folder per run and an `index.json` that lists the runs. If the index cannot be read, the server refuses to start. Move the file aside to start fresh: the next start then deletes the run folders that no index lists. Two servers cannot use one work directory.

## Retention

**A run is deleted 48 hours after it finishes.** That removes the uploaded documents, the merged document, both reports, the progress log, and any model answer the run kept because it could not be read. The period starts when the run finishes, so a run made at the end of one working day is still there the next morning.

- `--retention SECONDS` or `LLOSSLESS_RETENTION` changes the period, and `--retention 0` keeps runs until someone deletes them.
- Under a finished run's download buttons, the page says how long runs are kept and how long this one has left.
- In the last quarter of the period, and at most 4 hours before the end, that sentence becomes a warning: "Download anything you want to keep."
- After deletion the download buttons are gone, and the page says the run was deleted. A short record that the run existed is kept for one more period, so an old link is answered with "deleted" and not with "not found".
- `DELETE /api/v1/runs/{id}` deletes a run before its time.

## Languages

The page speaks English and German. Choose with the globe at the top right. The choice is remembered in the browser. Without a choice, the browser's language setting decides, and English is the fallback.

Only the page is translated. The merged document, `report.json` and `report.html` are the same bytes whatever language the page is in, and the report, the command line and the model notes in the scorecard stay English.

## What a request may choose

A run submitted from the page or through the API may choose its documents and their base, its models, the fidelity level, the verification depth, the title policy, the loss budget and a context window. It may name one of this server's endpoints or subscription routes, and a merge effort for a route.

It may not supply an endpoint address, a command, the name of the variable a key is read from, or any path on the server. A request that could set an address would send the operator's key to a server of the submitter's choosing, and one that could set a command would run a program of the submitter's choosing. A request with an unknown field is refused.

## The JSON API

Everything the page does goes through a JSON API under `/api/v1/`, and a script can use it the same way. A script signs in with `"token": true` in the body. The answer then carries the session id as `token`, and the script sends it in an `X-LLossless-Token` header:

```sh
# sign in: the answer contains "token"
curl -s -H 'Content-Type: application/json' \
  -d '{"username": "me", "password": "my password", "token": true}' \
  http://127.0.0.1:8765/api/v1/session

# submit a run: the answer contains the run's "id"
curl -s -H 'Content-Type: application/json' -H "X-LLossless-Token: $TOKEN" \
  -d '{"documents": [{"name": "a.md", "text": "..."}, {"name": "b.md", "text": "..."}], "model": "qwen3:8b", "merge_model": "qwen3:8b"}' \
  http://127.0.0.1:8765/api/v1/runs

# ask for its state, and for the report once it is done
curl -s -H "X-LLossless-Token: $TOKEN" http://127.0.0.1:8765/api/v1/runs/$ID
```

The fields of a run are `documents` (a list of `name` and `text`, in order), `base`, `model` (the checks), `merge_model`, `fidelity`, `verify_depth`, `title_policy`, `loss_budget`, `window`, `endpoint`, `command_route` and `effort`. `GET /api/v1/config` lists the values this server accepts.

Every `POST`, `PUT` and `DELETE` must carry `Content-Type: application/json`, also when it has no body, for example `curl -X DELETE -H 'Content-Type: application/json' -H "X-LLossless-Token: $TOKEN" http://127.0.0.1:8765/api/v1/runs/$ID`.

The paths in the tables below are relative to `/api/v1`.

### Session and accounts

| method and path | what it does | answers |
|---|---|---|
| `GET /session` | Whether the server has accounts, whether it needs setup, and who is signed in. Needs no sign-in. | 200 |
| `POST /session` | Sign in with `username` and `password`. Needs no sign-in. | 200 and a cookie; 401 `bad_login` |
| `DELETE /session` | Sign out. | 204 |
| `POST /setup` | Create the first account with `token` (the code from the one-time address), `username` and `password`. Works once. | 200; 403 `bad_setup_token`; 409 `already_set_up` |
| `GET /accounts` | List the accounts. Operator only. | 200 |
| `POST /accounts` | Add an account with `username` and `password`, and `"operator": true` for an operator. Operator only. | 201 |
| `DELETE /accounts/{name}` | Remove an account and the keys it stored, and cancel its queued and running runs. Operator only. | 204 |
| `PUT /accounts/{name}/password` | Set a new `password`. Your own needs `current` as well. An operator can set anybody's. | 204; 403 `bad_current_password` |

### Server and settings

| method and path | what it does | answers |
|---|---|---|
| `GET /health` | The version, which keys are set, and who is asking. | 200 |
| `GET /config` | Everything the page's controls are built from: levels, depths, title policies, the model list, endpoints, subscription routes by id, languages, size limits and the retention period. | 200 |
| `GET /locales`, `GET /locales/{tag}` | The page's texts, in the browser's language or in a named one. Needs no sign-in. | 200; 404 `no_locale` |
| `GET /defaults` | Your saved settings, and the ones this server no longer offers. | 200 |
| `PUT /defaults` | Save settings. Each one is checked against what this server offers. | 200; 400 `bad_defaults` |
| `DELETE /defaults` | Remove your saved settings. | 204 |
| `GET /settings/keys` | Per provider: whether a key is set, the endpoint (scheme, host and port only when a member looks at an operator's endpoint), and the last four characters of a key that belongs to the account asking. | 200 |
| `PUT /settings/keys/{name}` | Store a key: `{"key": "..."}`. | 204; 403 `no_endpoint_of_your_own` |
| `DELETE /settings/keys/{name}` | Remove a provider's key. | 204 |
| `PUT /settings/endpoints/{name}` | Store an endpoint: `{"base_url": "..."}`. Clears that provider's key and answers with the models the endpoint listed. | 200; 400 `bad_endpoint` |
| `DELETE /settings/endpoints/{name}` | Remove a provider's endpoint, its key and its model list. | 204 |
| `PUT /settings/commands/{name}` | Switch on a subscription tool the server found. Operator only. | 200; 400 `bad_command_tool` |
| `DELETE /settings/commands/{name}` | Switch it off. A route written by hand is never touched. Operator only. | 200 |

`{name}` is a provider (`anthropic`, `google`, `openai`, `self-hosted`) on the keys and endpoints routes, and a tool id such as `claude-opus` on the commands routes.

### Runs

| method and path | what it does | answers |
|---|---|---|
| `POST /runs` | Submit documents and settings. The run is queued. | 202, the run's `id` and a `Location` header; 400 with the reason |
| `GET /runs` | Your runs. | 200 |
| `GET /runs/{id}` | State, times, exit code, place in the queue, seconds until deletion, and the report once there is one. | 200 |
| `DELETE /runs/{id}` | Delete a run and everything it produced. | 204 |
| `POST /runs/{id}/cancel` | Cancel a queued or running run. Its submitter or an operator. | 202; 409 `not_running` |
| `POST /runs/{id}/retry` | Start a new run from a failed or interrupted one. Its submitter only. | 202 and a `Location` header; 409 `not_retryable`; 410 `forgotten` |
| `GET /runs/{id}/events` | Progress as Server-Sent Events. Honours `Last-Event-ID`. | 200 |
| `GET /runs/{id}/merged` | The merged document, as markdown. | 200 |
| `GET /runs/{id}/report.html` | The HTML report as a file to keep. | 200 |
| `GET /runs/{id}/report` | The same report as a page to read, with a button that saves it. | 200 |
| `GET /runs/{id}/bundle.zip` | The documents, the merged document, `report.json` and `report.html` in one zip. | 200 |

The last four routes answer 409 `not_finished` while the run is going, 404 `no_artefact` when the run produced no such file, and 410 `forgotten` after the run was deleted.

### Answers that apply everywhere

- An error is `{"error": {"code": "...", "message": "..."}}`.
- 401 `no_session`: not signed in. 401 `setup_required`: the server has no account yet.
- 403 `not_operator`: the route is the operator's.
- 404 `no_run`: no such run, or it is somebody else's. 400 `bad_id`: a run id is 32 hexadecimal characters.
- 400 `unknown_field`: the body has a field the API does not define.
- 403 `cross_origin`: the request's `Origin` header does not name this server.
- 405 `wrong_method`, 411 `length_required` (a body needs a `Content-Length`), 413 `body_too_large` (over about 4 MB, and over 64 KB on `session` and `setup`), 415 `not_json` (every `POST`, `PUT` and `DELETE` declares `application/json`, with or without a body).

A report served by the API has the server's own directory paths removed, and so have a run's error message and its progress stream. The merged document and your documents are served exactly as they are.

## Security details

For a reviewer: the mechanisms behind what the sections above describe.

**Signing in**

- A session id is 256 random bits from `secrets.token_urlsafe`. It is kept in the server's memory only and compared with `hmac.compare_digest`.
- The browser holds it in the cookie `llossless_session`, set `HttpOnly`, `SameSite=Strict` and `Path=/`, and `Secure` when the request arrived with `X-Forwarded-Proto: https`. A script presents the same id in `X-LLossless-Token`.
- A session ends after 12 hours without use, after 7 days, on sign-out, on a password change, when the account is removed, and when the server stops.
- Passwords are hashed with `hashlib.scrypt` (N = 2^14, r = 8, p = 1), or with PBKDF2-HMAC-SHA256 at 600,000 rounds where scrypt is not available, with a 16-byte salt per account. The cost is stored with each record, so it can be raised later.
- An unknown username and a wrong password get the same answer and take about the same time: the hash is computed either way. After 10 failed sign-ins for one name within 5 minutes, further attempts for that name get that same answer, until 5 minutes pass without a failure. A wrong `current` password on a password change counts as a failed sign-in for that name.

**Requests**

- Only three routes answer without a sign-in: `session`, `setup` and `locales`. The list is exact, not a prefix. The page's own files are public and hold no data.
- Cross-site request forgery: the cookie is `SameSite=Strict`. Every `POST`, `PUT` and `DELETE` must declare `application/json`, and an `Origin` header on one of them must name this server's own scheme, host and port: the `Host` header, under `https` when a proxy sent `X-Forwarded-Proto: https`. `Origin: null` is refused. A request with no `Origin` header, which is how a script sends one, is accepted.
- A connection that sends nothing for 60 seconds is closed, and a request from somebody who is not signed in is answered before its body is read.
- DNS rebinding: a server bound to this machine's own address refuses any request whose `Host` header is not `127.0.0.1`, `localhost` or `::1`. A server bound to a network address does not make this check.
- Every response carries `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer` and a content security policy that allows scripts from the server itself only. The HTML report is served in a sandbox, so it cannot read anything else the server holds.
- The page puts text from documents and models on screen as text, never as HTML.

**Tokens, keys and files**

- The setup code is 256 random bits. It travels in the URL fragment, which browsers do not send to a server, so it reaches no log. It is never written to disk.
- `LLOSSLESS_WEB_TOKEN` is checked before the port is opened: without a valid token or an account, a network address is never bound. A token with a character outside ASCII is refused at start, because a browser and a script would send it as different bytes.
- A run's address and its key are taken from one reading of the settings when the run starts, and a stored key is handed out only for the address it is stored with. Changing an endpoint while a run is under way can therefore never send a key to an address it was not saved for. That includes this server's own endpoint. The one exception is a key given as an environment variable, which has no stored address.
- An endpoint's error text is shown with anything shaped like a key removed, including the start and the end of the key that was sent.
- While a server has a token and no account, every API request without the token is refused with 401 `no_token`, the three routes that need no sign-in included. The page holds the token the reader typed in a script variable only: it is never written to browser storage or to the address. The page sends it in `X-LLossless-Token` and drops it when the server reports an account, because from then on that header carries a session id.
- No route returns a key, and no key is written to a log, a report or a JSON answer. The last four characters of a key are sent only to the account that owns it, so a member's answer about a shared key says that it is set and nothing else. A member's keys never enter the server's environment: they are read from that member's file when the run starts and are sent only to the address that member stored them with.
- The accounts file, the credentials files, the commands file and the work directory are created for their owner only (mode `0600` for files, `0700` for directories). A credentials or commands file that others can read is refused, not repaired: its keys may already have been read and should be replaced. A `users` folder that an earlier version created with wider permissions is set to `0700` at start.

**What is not protected**

- There is no limit on what an account spends or on how many runs it submits, and the server does not encrypt its connections.
- A subscription route runs a program with the server's own login. Everything that program can do, a run through it can cause.

## For contributors

- **Code.** The web interface is `src/llossless/web/`. `api.py` holds the JSON contract as plain functions with no sockets, `server.py` is the HTTP layer, and `jobs.py` is the queue and retention. The page is `static/index.html` and `static/app.js`, with no build step.
- **Tests.** The web tests are `tests/test_web_server.py` and the files named like it. They call no model: a test that needs a server or a model endpoint starts one on a free local port. `tests/test_web_jobs.py` runs one merge through the web job layer and one through the command line against the same endpoint, and requires the two reports to agree.
- **Model figures.** The picker, the scorecard and the merge-effort card read `src/llossless/web/catalogue.json`. The runs behind the merge-effort figures are in `arms/2026-09-25/subscription-comparison/` and `arms/2026-09-26/opus-max/`, and `tests/effort_figures.py --check` and `tests/opus55_effort_figures.py --check` compare the two.
- **Adding a language.** Copy `src/llossless/web/locales/en.json`, translate the values, and run `python3 tests/test_web_i18n.py`. It names every key that is missing and every placeholder that was renamed. A language file with a missing key is refused whole.
- **A run folder** holds `sources.json` (the documents as submitted), `events.jsonl` (the progress log), `merged.md`, `report.json` and `report.html`, and `failures/` and `discards/` when a model's answer could not be read.
