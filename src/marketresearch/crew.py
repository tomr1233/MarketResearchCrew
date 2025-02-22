from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import yaml
from crewai_tools import (
    WebsiteSearchTool,
    FirecrawlScrapeWebsiteTool,
    CSVSearchTool,
    PDFSearchTool,
)

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Marketresearch():
	"""Marketresearch crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
    
    # Define worker agents using the @agent decorator
	@agent
	def research_planner(self) -> Agent:
		return Agent(
			config=self.agents_config['research_planner'], 
			verbose=True
		)
		
	@agent
	def data_collector(self) -> Agent:
		tools=[WebsiteSearchTool(), FirecrawlScrapeWebsiteTool()]
		return Agent(
			config=self.agents_config['data_collector'], 
			verbose=True
		)
		
	@agent
	def data_analyst(self) -> Agent:
		tools=[PDFSearchTool(), CSVSearchTool()]
		return Agent(
			config=self.agents_config['data_analyst'], 
			verbose=True
		)
		
	@agent
	def report_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['report_writer'], 
			verbose=True
		)
		
	@agent
	def quality_checker(self) -> Agent:
		return Agent(
			config=self.agents_config['quality_checker'], 
			verbose=True
		)
		
		# Define tasks using the @task decorator
	@task
	def research_planning_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_planning_task']
		)

	@task
	def data_collection_task(self) -> Task:
		return Task(
			config=self.tasks_config['data_collection_task']
		)
		
	@task
	def data_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['data_analysis_task'],
		)
		
	@task
	def market_report_task(self) -> Task:
		return Task(
			config=self.tasks_config['market_report_task'], 
			output_file="report.md"
		)
		
	@task
	def quality_check_task(self) -> Task:
		return Task(
			config=self.tasks_config['quality_check_task']
		)
		
		# Define the crew with hierarchical process and manager agent
	@crew
	def crew(self) -> Crew:
		# Create the manager agent separately
		manager_agent = Agent(config=self.agents_config['project_manager'], 
								verbose=True
		)
			
		return Crew(
			agents=self.agents,  # Worker agents defined with @agent
			tasks=self.tasks,    # Tasks defined with @task
			process=Process.hierarchical,
			manager_agent=manager_agent,
			verbose=True
		)