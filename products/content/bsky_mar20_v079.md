# Bluesky Post — Mar 20 v0.79.0 (too_many_params)

the Snyk security scanner MCP tool has 34 parameters.

thirty. four.

target_file, dev, all_projects, detection_depth, exclude, prune_repeated_subdependencies, print_deps, print_dep_paths, show_vulnerable_paths, project_name, target_reference...

models don't reliably fill 34 fields. they omit things. they guess.

agent-friend v0.79.0 now flags this. snyk drops to 7.3/100.

pip install agent-friend
