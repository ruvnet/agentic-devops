import re
import asyncio
from lionagi import Session, Branch, iModel, pile
from concurrent.futures import ThreadPoolExecutor
from .utils import *

async def initialize_lionagi_session(imodel=None):
    system = "You are an assistant designed to help with DevOps tasks."
    return Session(system=system, imodel=imodel)

async def handle_user_input(session: Session, user_input: str | dict, imodel=None, imodel_kwagrs={}):
    if not imodel:
        imodel = session.imodel or iModel(model="gpt-4o", **imodel_kwagrs)
    
    # better to use a string or instruction node object than dictionary for single
    # instruction, as internally we will indicate the instruction to the model
    # no need to add extra tokens
    instruction = "Interpret the task and generate appropriate responses or actions."

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
            system = "You are an assistant designed to help with DevOps tasks."
            
            # use branch for concurrent execution
            branch = Branch(system=system, imodel=imodel)
            result = await branch.chat(instruction=instruction, context=chunk)
            return result, branch

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
        results = [result for result, branch in review_results]
        branches = [branch for result, branch in review_results]
        session.branches.include(branches)
        
        verbose_output("\n🦁 LionAGI review:")
        for result in results:
            verbose_output(result)

        verbose_output("\n🤔 Generating potential actions based on the request...")
        action_prompt = {
            "User request": user_input,
            "Directory information": files_and_dirs,
        }

        # use a new branch if you don't need previous messages as given context
        # for current task
        branch = session.new_branch()
        potential_actions = await branch.chat(
            instruction=instruction, 
            context=action_prompt
        )

        verbose_output("\n📝 Potential actions:")
        verbose_output(potential_actions)

        execute_action = click.confirm("Do you want to execute any of the suggested actions?")
        if execute_action:
            selected_action = click.prompt("Enter the action you want to execute", type=str)
            verbose_output(f"\n⚙️ Executing: {selected_action}")
            subprocess.run(selected_action, shell=True, check=True)
        else:
            verbose_output("\n⏭️ Skipping action execution.")
        
        # saving all messages across all branches to a dataframe
        # messages = pile()
        # for b in session.branches:
        #     messages += b.messages
        # df = messages.to_df()
        # df.to_csv()
        
        # return " ".join(results)
    except subprocess.CalledProcessError as e:
        verbose_output(f"\n⚠️ Error: {e.output}")
    except Exception as e:
        verbose_output(f"\n⚠️ Error: {e}")
