import os
import random
import sys

import streamlit as st

from aider.coders import Coder
from aider.dump import dump  # noqa: F401
from aider.io import InputOutput
from aider.main import main as cli_main
from aider.scrape import Scraper

class CaptureIO(InputOutput):
    lines = []

    def tool_output(self, msg):
        self.lines.append(msg)

    def tool_error(self, msg):
        self.lines.append(msg)

    def get_captured_lines(self):
        lines = self.lines
        self.lines = []
        return lines

def search(text=None):
    results = []
    for root, _, files in os.walk("aider"):
        for file in files:
            path = os.path.join(root, file)
            if not text or text in path:
                results.append(path)
    return results

class State:
    keys = set()

    def init(self, key, val=None):
        if key in self.keys:
            return

        self.keys.add(key)
        setattr(self, key, val)
        return True

@st.cache_resource
def get_state():
    return State()

@st.cache_resource
def get_coder():
    coder = cli_main(return_coder=True)
    if not isinstance(coder, Coder):
        raise ValueError(coder)
    if not coder.repo:
        raise ValueError("GUI can currently only be used inside a git repo")

    io = CaptureIO(
        pretty=False,
        yes=True,
        dry_run=coder.io.dry_run,
        encoding=coder.io.encoding,
    )
    coder.commands.io = io

    return coder

class GUI:
    prompt = None
    prompt_as = "user"
    last_undo_empty = None
    recent_msgs_empty = None
    web_content_empty = None

    def announce(self):
        lines = self.coder.get_announcements()
        lines = "  \n".join(lines)
        return lines

    def show_edit_info(self, edit):
        commit_hash = edit.get("commit_hash")
        commit_message = edit.get("commit_message")
        diff = edit.get("diff")
        fnames = edit.get("fnames")
        if fnames:
            fnames = sorted(fnames)

        if not commit_hash and not fnames:
            return

        show_undo = False
        res = ""
        if commit_hash:
            prefix = "aider: "
            if commit_message.startswith(prefix):
                commit_message = commit_message[len(prefix) :]
            res += f"Commit `{commit_hash}`: {commit_message}  \n"
            if commit_hash == self.coder.last_aider_commit_hash:
                show_undo = True

        if fnames:
            fnames = [f"`{fname}`" for fname in fnames]
            fnames = ", ".join(fnames)
            res += f"Applied edits to {fnames}."

        if diff:
            with st.expander(res):
                st.code(diff, language="diff")
                if show_undo:
                    self.add_undo(commit_hash)
        else:
            with st.container(border=True):
                st.write(res)
                if show_undo:
                    self.add_undo(commit_hash)

    def add_undo(self, commit_hash):
        if self.last_undo_empty:
            self.last_undo_empty.empty()

        self.last_undo_empty = st.empty()
        undone = self.state.last_undone_commit_hash == commit_hash
        if not undone:
            with self.last_undo_empty:
                if self.button(f"Undo commit `{commit_hash}`", key=f"undo_{commit_hash}"):
                    self.do_undo(commit_hash)

    def do_sidebar(self):
        with st.sidebar:
            st.title("Agentic Devops")
            st.caption("Version 0.01rc")

            # Add a dropdown menu for features
            feature = st.selectbox(
                "Select a Feature",
                [
                    "Select a Feature",
                    "Create Dockerfile",
                    "Create Bash Script",
                    "Create Kubernetes Configuration",
                    "Create CI/CD Pipeline",
                    "Azure Configuration",
                    "AWS Configuration",
                    "GCP Configuration",
                    "Firebase Configuration",
                    "Developer Configuration"
                ]
            )

            additional_input = ""
            if feature != "Select a Feature":
                if feature == "Create Dockerfile":
                    additional_input = st.text_area("Dockerfile Options", "Enter Dockerfile options")
                    base_image = st.text_input("Base Image", "e.g., python:3.8-slim")
                    maintainer = st.text_input("Maintainer", "e.g., Your Name <you@example.com>")
                    packages = st.text_input("Packages to Install", "e.g., build-essential")
                    commands = st.text_input("Commands to Run", "e.g., pip install -r requirements.txt")
                    additional_input = f"{additional_input}, Base Image: {base_image}, Maintainer: {maintainer}, Packages: {packages}, Commands: {commands}"
                elif feature == "Create Bash Script":
                    additional_input = st.text_area("Bash Script Details", "Enter script details")
                    script_name = st.text_input("Script Name", "e.g., deploy.sh")
                    description = st.text_input("Description", "e.g., A script to deploy the application")
                    additional_input = f"{additional_input}, Script Name: {script_name}, Description: {description}"
                elif feature == "Create Kubernetes Configuration":
                    additional_input = st.text_area("Kubernetes Config Details", "Enter config details")
                    deployment_name = st.text_input("Deployment Name", "e.g., my-app")
                    image = st.text_input("Container Image", "e.g., my-app:latest")
                    replicas = st.number_input("Replicas", 1, 10, 1)
                    additional_input = f"{additional_input}, Deployment Name: {deployment_name}, Image: {image}, Replicas: {replicas}"
                elif feature == "Create CI/CD Pipeline":
                    additional_input = st.text_area("CI/CD Pipeline Details", "Enter pipeline details")
                    pipeline_name = st.text_input("Pipeline Name", "e.g., Build and Deploy")
                    stages = st.text_input("Stages", "e.g., build, test, deploy")
                    additional_input = f"{additional_input}, Pipeline Name: {pipeline_name}, Stages: {stages}"
                elif feature == "Azure Configuration":
                    additional_input = st.text_area("Azure Config Details", "Enter Azure config details")
                    resource_group = st.text_input("Resource Group", "e.g., my-resource-group")
                    location = st.text_input("Location", "e.g., eastus")
                    additional_input = f"{additional_input}, Resource Group: {resource_group}, Location: {location}"
                elif feature == "AWS Configuration":
                    additional_input = st.text_area("AWS Config Details", "Enter AWS config details")
                    stack_name = st.text_input("Stack Name", "e.g., my-stack")
                    region = st.text_input("Region", "e.g., us-east-1")
                    additional_input = f"{additional_input}, Stack Name: {stack_name}, Region: {region}"
                elif feature == "GCP Configuration":
                    additional_input = st.text_area("GCP Config Details", "Enter GCP config details")
                    project_id = st.text_input("Project ID", "e.g., my-project-id")
                    zone = st.text_input("Zone", "e.g., us-central1-a")
                    additional_input = f"{additional_input}, Project ID: {project_id}, Zone: {zone}"
                elif feature == "Firebase Configuration":
                    additional_input = st.text_area("Firebase Config Details", "Enter Firebase config details")
                    project_id = st.text_input("Project ID", "e.g., my-firebase-project")
                    api_key = st.text_input("API Key", "e.g., my-api-key")
                    additional_input = f"{additional_input}, Project ID: {project_id}, API Key: {api_key}"
                elif feature == "Developer Configuration":
                    additional_input = st.text_area("Developer Config Details", "Enter developer config details")
                    nixpkgs_version = st.text_input("Nixpkgs Version", "e.g., 21.05")
                    packages = st.text_input("Packages to Install", "e.g., vim, git")
                    additional_input = f"{additional_input}, Nixpkgs Version: {nixpkgs_version}, Packages: {packages}"

            if st.button("Start"):
                self.start_feature(feature, additional_input)

            self.do_add_to_chat()
            self.do_recent_msgs()
            self.do_clear_chat_history()

            st.warning(
                "This browser version of Agentic Devops is experimental. Please share feedback in [GitHub"
                " issues](https://github.com/ruvnet/agentic-devops/issues)."
            )

    def start_feature(self, feature, additional_input):
        internal_guidance = ""
        
        if feature == "Create Dockerfile":
            internal_guidance = "Ensure to include best practices for Dockerfile creation, such as minimizing layers, using a small base image, and cleaning up unnecessary files."
            self.prompt = f"Create a Dockerfile with options: {additional_input}. {internal_guidance}"
        elif feature == "Create Bash Script":
            internal_guidance = "The script should handle errors gracefully, use descriptive comments, and include execution permissions."
            self.prompt = f"Create a basic deployment script with details: {additional_input}. {internal_guidance}"
        elif feature == "Create Kubernetes Configuration":
            internal_guidance = "Ensure the configuration includes resource limits, readiness and liveness probes, and follows Kubernetes best practices."
            self.prompt = f"Create a Kubernetes config for a web application with details: {additional_input}. {internal_guidance}"
        elif feature == "Create CI/CD Pipeline":
            internal_guidance = "The pipeline should include stages for building, testing, and deploying the application, and should support rollback mechanisms."
            self.prompt = f"Create a CI/CD pipeline for a Python project with details: {additional_input}. {internal_guidance}"
        elif feature == "Azure Configuration":
            internal_guidance = "Include detailed resource definitions, dependencies, and parameterized templates for flexibility."
            self.prompt = f"Create an Azure Resource Manager template with details: {additional_input}. {internal_guidance}"
        elif feature == "AWS Configuration":
            internal_guidance = "Ensure the template includes IAM roles and policies, and follows AWS best practices for security and scalability."
            self.prompt = f"Create a CloudFormation template with details: {additional_input}. {internal_guidance}"
        elif feature == "GCP Configuration":
            internal_guidance = "Include configurations for IAM, networking, and resource management according to Google Cloud best practices."
            self.prompt = f"Create a Google Cloud Deployment Manager template with details: {additional_input}. {internal_guidance}"
        elif feature == "Firebase Configuration":
            internal_guidance = "Ensure the configuration includes authentication, database rules, and hosting settings."
            self.prompt = f"Create a Firebase configuration with details: {additional_input}. {internal_guidance}"
        elif feature == "Developer Configuration":
            internal_guidance = "Include common development tools and configurations, ensuring they follow best practices for development environments."
            self.prompt = f"Create a .nix configuration with details: {additional_input}. {internal_guidance}"

        if self.prompt:
            self.state.prompt = self.prompt
            self.process_chat()



    def do_settings_tab(self):
        pass

    def do_recommended_actions(self):
        with st.expander("Recommended actions", expanded=True):
            with st.popover("Create a git repo to track changes"):
                st.write(
                    "Aider works best when your code is stored in a git repo.  \n[See the FAQ"
                    " for more info](https://aider.chat/docs/faq.html#how-does-aider-use-git)"
                )
                self.button("Create git repo", key=random.random(), help="?")

            with st.popover("Update your `.gitignore` file"):
                st.write("It's best to keep aider's internal files out of your git repo.")
                self.button("Add `.aider*` to `.gitignore`", key=random.random(), help="?")

    def do_add_to_chat(self):
        self.do_add_files()
        self.do_add_web_page()

    def do_add_files(self):
        fnames = st.multiselect(
            "Add files to the chat",
            self.coder.get_all_relative_files(),
            default=self.state.initial_inchat_files,
            placeholder="Files to edit",
            disabled=self.prompt_pending(),
            help=(
                "Only add the files that need to be *edited* for the task you are working"
                " on. Aider will pull in other relevant code to provide context to the LLM."
            ),
        )

        for fname in fnames:
            if fname not in self.coder.get_inchat_relative_files():
                self.coder.add_rel_fname(fname)
                self.info(f"Added {fname} to the chat")

        for fname in self.coder.get_inchat_relative_files():
            if fname not in fnames:
                self.coder.drop_rel_fname(fname)
                self.info(f"Removed {fname} from the chat")

    def do_add_web_page(self):
        with st.popover("Add a web page to the chat"):
            self.do_web()

    def do_add_image(self):
        with st.popover("Add image"):
            st.markdown("Hello World 👋")
            st.file_uploader("Image file", disabled=self.prompt_pending())

    def do_run_shell(self):
        with st.popover("Run shell commands, tests, etc"):
            st.markdown(
                "Run a shell command and optionally share the output with the LLM. This is"
                " a great way to run your program or run tests and have the LLM fix bugs."
            )
            st.text_input("Command:")
            st.radio(
                "Share the command output with the LLM?",
                [
                    "Review the output and decide whether to share",
                    "Automatically share the output on non-zero exit code (ie, if any tests fail)",
                ],
            )
            st.selectbox(
                "Recent commands",
                [
                    "my_app.py --doit",
                    "my_app.py --cleanup",
                ],
                disabled=self.prompt_pending(),
            )

    def do_tokens_and_cost(self):
        with st.expander("Tokens and costs", expanded=True):
            pass

    def do_show_token_usage(self):
        with st.popover("Show token usage"):
            st.write("hi")

    def do_clear_chat_history(self):
        text = "Saves tokens, reduces confusion"
        if self.button("Clear chat history", help=text):
            self.coder.done_messages = []
            self.coder.cur_messages = []
            self.info("Cleared chat history. Now the LLM can't see anything before this line.")

    def do_show_metrics(self):
        st.metric("Cost of last message send & reply", "$0.0019", help="foo")
        st.metric("Cost to send next message", "$0.0013", help="foo")
        st.metric("Total cost this session", "$0.22")

    def do_git(self):
        with st.expander("Git", expanded=False):
            self.button("Commit any pending changes")
            with st.popover("Run git command"):
                st.markdown("## Run git command")
                st.text_input("git", value="git ")
                self.button("Run")
                st.selectbox(
                    "Recent git commands",
                    [
                        "git checkout -b experiment",
                        "git stash",
                    ],
                    disabled=self.prompt_pending(),
                )

    def do_recent_msgs(self):
        if not self.recent_msgs_empty:
            self.recent_msgs_empty = st.empty()

        if self.prompt_pending():
            self.recent_msgs_empty.empty()
            self.state.recent_msgs_num += 1

        with self.recent_msgs_empty:
            self.old_prompt = st.selectbox(
                "Resend a recent chat message",
                self.state.input_history,
                placeholder="Choose a recent chat message",
                index=None,
                key=f"recent_msgs_{self.state.recent_msgs_num}",
                disabled=self.prompt_pending(),
            )
            if self.old_prompt:
                self.prompt = self.old_prompt

    def do_messages_container(self):
        self.messages = st.container()

        with self.messages:
            for msg in self.state.messages:
                role = msg["role"]

                if role == "edit":
                    self.show_edit_info(msg)
                elif role == "info":
                    st.info(msg["content"])
                elif role == "text":
                    text = msg["content"]
                    line = text.splitlines()[0]
                    with self.messages.expander(line):
                        st.text(text)
                elif role in ("user", "assistant"):
                    with st.chat_message(role):
                        st.write(msg["content"])
                else:
                    st.dict(msg)

    def initialize_state(self):
        messages = [
            dict(role="info", content=self.announce()),
            dict(role="assistant", content="How can I help you?"),
        ]

        self.state.init("messages", messages)
        self.state.init("last_aider_commit_hash", self.coder.last_aider_commit_hash)
        self.state.init("last_undone_commit_hash")
        self.state.init("recent_msgs_num", 0)
        self.state.init("web_content_num", 0)
        self.state.init("prompt")
        self.state.init("scraper")

        self.state.init("initial_inchat_files", self.coder.get_inchat_relative_files())

        if "input_history" not in self.state.keys:
            input_history = list(self.coder.io.get_input_history())
            seen = set()
            input_history = [x for x in input_history if not (x in seen or seen.add(x))]
            self.state.input_history = input_history
            self.state.keys.add("input_history")

    def button(self, args, **kwargs):
        "Create a button, disabled if prompt pending"
        if self.prompt_pending():
            kwargs["disabled"] = True
        return st.button(args, **kwargs)

    def __init__(self):
        self.coder = get_coder()
        self.state = get_state()

        self.coder.yield_stream = True
        self.coder.stream = True
        self.coder.pretty = False

        self.initialize_state()

        self.do_messages_container()
        self.do_sidebar()

        user_inp = st.chat_input("Say something")
        if user_inp:
            self.prompt = user_inp

        if self.prompt_pending():
            self.process_chat()

        if not self.prompt:
            return

        self.state.prompt = self.prompt

        if self.prompt_as == "user":
            self.coder.io.add_to_input_history(self.prompt)

        self.state.input_history.append(self.prompt)

        if self.prompt_as:
            self.state.messages.append({"role": self.prompt_as, "content": self.prompt})
        if self.prompt_as == "user":
            with self.messages.chat_message("user"):
                st.write(self.prompt)
        elif self.prompt_as == "text":
            line = self.prompt.splitlines()[0]
            line += "??"
            with self.messages.expander(line):
                st.text(self.prompt)

        st.rerun()

    def prompt_pending(self):
        return self.state.prompt is not None

    def cost(self):
        cost = random.random() * 0.003 + 0.001
        st.caption(f"${cost:0.4f}")

    def process_chat(self):
        prompt = self.state.prompt
        self.state.prompt = None

        while prompt:
            with self.messages.chat_message("assistant"):
                res = st.write_stream(self.coder.run_stream(prompt))
                self.state.messages.append({"role": "assistant", "content": res})
            if self.coder.reflected_message:
                self.info(self.coder.reflected_message)
            prompt = self.coder.reflected_message

        with self.messages:
            edit = dict(
                role="edit",
                fnames=self.coder.aider_edited_files,
            )
            if self.state.last_aider_commit_hash != self.coder.last_aider_commit_hash:
                edit["commit_hash"] = self.coder.last_aider_commit_hash
                edit["commit_message"] = self.coder.last_aider_commit_message
                commits = f"{self.coder.last_aider_commit_hash}~1"
                diff = self.coder.repo.diff_commits(
                    self.coder.pretty,
                    commits,
                    self.coder.last_aider_commit_hash,
                )
                edit["diff"] = diff
                self.state.last_aider_commit_hash = self.coder.last_aider_commit_hash

            self.state.messages.append(edit)
            self.show_edit_info(edit)

        st.rerun()

    def info(self, message, echo=True):
        info = dict(role="info", content=message)
        self.state.messages.append(info)
        if echo:
            self.messages.info(message)

    def do_web(self):
        st.markdown("Add the text content of a web page to the chat")

        if not self.web_content_empty:
            self.web_content_empty = st.empty()

        if self.prompt_pending():
            self.web_content_empty.empty()
            self.state.web_content_num += 1

        with self.web_content_empty:
            self.web_content = st.text_input(
                "URL",
                placeholder="https://...",
                key=f"web_content_{self.state.web_content_num}",
            )

        if not self.web_content:
            return

        url = self.web_content

        if not self.state.scraper:
            self.scraper = Scraper(print_error=self.info)

        instructions = self.scraper.get_playwright_instructions()
        if instructions:
            self.info(instructions)

        content = self.scraper.scrape(url) or ""
        if content.strip():
            content = f"{url}\n\n" + content
            self.prompt = content
            self.prompt_as = "text"
        else:
            self.info(f"No web content found for `{url}`.")
            self.web_content = None

    def do_undo(self, commit_hash):
        self.last_undo_empty.empty()

        if (
            self.state.last_aider_commit_hash != commit_hash
            or self.coder.last_aider_commit_hash != commit_hash
        ):
            self.info(f"Commit `{commit_hash}` is not the latest commit.")
            return

        self.coder.commands.io.get_captured_lines()
        reply = self.coder.commands.cmd_undo(None)
        lines = self.coder.commands.io.get_captured_lines()

        lines = "\n".join(lines)
        lines = lines.splitlines()
        lines = "  \n".join(lines)
        self.info(lines, echo=False)

        self.state.last_undone_commit_hash = commit_hash

        if reply:
            self.prompt_as = None
            self.prompt = reply

def gui_main():
    st.set_page_config(
        layout="wide",
        page_title="Agentic Devops 2",
        page_icon="https://aider.chat/assets/favicon-32x32.png",
        menu_items={
            "Get Help": "https://aider.chat/docs/faq.html",
            "Report a bug": "https://github.com/paul-gauthier/aider/issues",
            "About": "# Aider\nAI pair programming in your browser.",
        },
    )

    GUI()

if __name__ == "__main__":
    status = gui_main()
    sys.exit(status)
