# Import necessary modules and classes from various agent files and asyncio.
from agents import Runner, trace, gen_trace_id  # Runner for executing agents, trace for logging, gen_trace_id for unique trace IDs.
from search_agent import search_agent          # Agent responsible for performing web searches.
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan # Agent for planning searches, and data structures for search items and plans.
from writer_agent import writer_agent, ReportData # Agent for writing the final report, and data structure for report data.
from email_agent import email_agent            # Agent for sending email.
import asyncio                                 # Asynchronous programming library.

# Define the main class that orchestrates the research process.
class ResearchManager:

    async def run(self, query: str):
        """
        Runs the entire deep research process.
        This is an asynchronous generator function that yields status updates
        and the final report as the process progresses.
        """
        # Generate a unique trace ID for tracking the execution flow.
        trace_id = gen_trace_id()
        # Start a new trace context for logging the research process.
        with trace("Research trace", trace_id=trace_id):
            # Print the URL to view the trace on the OpenAI platform.
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            # Yield the trace URL as a status update to the caller.
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            # Print a status message indicating research has started.
            print("Starting research...")
            # Step 1: Plan the necessary web searches for the given query.
            search_plan = await self.plan_searches(query)
            # Yield a status update indicating searches are planned and starting.
            yield "Searches planned, starting to search..."    
            # Step 2: Execute the planned web searches.
            search_results = await self.perform_searches(search_plan)
            # Yield a status update indicating searches are complete and report writing is starting.
            yield "Searches complete, writing report..."
            # Step 3: Write the final report based on the original query and search results.
            report = await self.write_report(query, search_results)
            # Yield a status update indicating the report is written and email is being sent.
            yield "Report written, sending email..."
            # Step 4: Send an email containing the generated report.
            await self.send_email(report)
            # Yield a status update indicating the email has been sent and research is complete.
            yield "Email sent, research complete"
            # Yield the markdown content of the final report as the last output.
            yield report.markdown_report
        

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """
        Plans the web searches that need to be performed for the given query.
        It uses the 'planner_agent' to determine the search strategy.
        """
        print("Planning searches...")
        # Run the planner_agent with the query as input.
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        # Print the number of searches that will be performed.
        print(f"Will perform {len(result.final_output.searches)} searches")
        # Return the final output of the planner agent, cast to a WebSearchPlan object.
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """
        Performs the web searches as outlined in the search plan.
        It runs multiple searches concurrently using asyncio.
        """
        print("Searching...")
        num_completed = 0
        # Create a list of asynchronous tasks, one for each search item in the plan.
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []
        # Iterate over tasks as they complete (asynchronously).
        for task in asyncio.as_completed(tasks):
            # Await the result of the completed task.
            result = await task
            # If the search returned a result (not None), add it to the results list.
            if result is not None:
                results.append(result)
            # Increment the counter for completed searches.
            num_completed += 1
            # Print a progress update.
            print(f"Searching... {num_completed}/{len(tasks)} completed")
        print("Finished searching")
        # Return the list of search results.
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """
        Performs a single web search for a given WebSearchItem.
        It uses the 'search_agent' to execute the search.
        """
        # Construct the input string for the search agent, including the search term and reason.
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            # Run the search_agent with the constructed input.
            result = await Runner.run(
                search_agent,
                input,
            )
            # Return the final output of the search agent as a string.
            return str(result.final_output)
        except Exception:
            # If an error occurs during the search, return None.
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """
        Writes the final report based on the original query and the summarized search results.
        It uses the 'writer_agent' to generate the report.
        """
        print("Thinking about report...")
        # Construct the input string for the writer agent.
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        # Run the writer_agent with the input.
        result = await Runner.run(
            writer_agent,
            input,
        )

        print("Finished writing report")
        # Return the final output of the writer agent, cast to a ReportData object.
        return result.final_output_as(ReportData)
    
    async def send_email(self, report: ReportData) -> None:
        """
        Sends an email containing the generated report.
        It uses the 'email_agent' to send the email.
        """
        print("Writing email...")
        # Run the email_agent with the markdown content of the report.
        result = await Runner.run(
            email_agent,
            report.markdown_report,
        )
        print("Email sent")
        # Return the original report object (though the agent handles the sending).
        return report
