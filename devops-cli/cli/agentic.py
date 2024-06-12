import asyncio
from lionagi import Session
from concurrent.futures import ThreadPoolExecutor

async def initialize_lionagi_session():
    system = "You are an assistant designed to help with DevOps tasks."
    return Session([[system]])

async def handle_user_input(session, user_input):
    context = {"task": user_input}
    instruction = {"Action": "Interpret the task and generate appropriate responses or actions."}

    # Intelligent parsing of directory paths
    match = re.search(r'\.\./|./|[a-zA-Z0-9_/]+', user_input)
    if match:
        repo_path = match.group(0)
    else:
        repo_path = "."

    try:
        # Get directory structure
        verbose_output(f"\n🔍 Analyzing directory structure for {repo_path}...")
        files_and_dirs = subprocess.check_output(f"ls -lR {repo_path}", shell=True, text=True)

        # Chunk the directory information to fit the token limit
        max_tokens = 28192
        chunks = [files_and_dirs[i:i+max_tokens] for i in range(0, len(files_and_dirs), max_tokens)]

        # Function to review chunk
        async def review_chunk(chunk):
            verbose_output("\n🤖 Sending directory information to LionAGI for review...")
            result = await session.chat(instruction=instruction, context={"task": chunk}, model="gpt-4oo")
            return result

        # Process chunks concurrently
        async def process_chunks_concurrently(chunks):
            with ThreadPoolExecutor() as executor:
                loop = asyncio.get_event_loop()
                tasks = [
                    loop.run_in_executor(executor, review_chunk, chunk)
                    for chunk in chunks
                ]
                return await asyncio.gather(*tasks)

        review_results = await process_chunks_concurrently(chunks)

        verbose_output("\n🦁 LionAGI review:")
        for result in review_results:
            verbose_output(result)

        verbose_output("\n🤔 Generating potential actions based on the request...")
        action_prompt = f"User request: {user_input}\nDirectory information:\n{files_and_dirs}"
        potential_actions = await session.chat(instruction=instruction, context={"task": action_prompt}, model="gpt-4oo")

        verbose_output("\n📝 Potential actions:")
        verbose_output(potential_actions)

        execute_action = click.confirm("Do you want to execute any of the suggested actions?")
        if execute_action:
            selected_action = click.prompt("Enter the action you want to execute", type=str)
            verbose_output(f"\n⚙️ Executing: {selected_action}")
            subprocess.run(selected_action, shell=True, check=True)
        else:
            verbose_output("\n⏭️ Skipping action execution.")

    except subprocess.CalledProcessError as e:
        verbose_output(f"\n⚠️ Error: {e.output}")
    except Exception as e:
        verbose_output(f"\n⚠️ Error: {e}")
