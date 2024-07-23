using Pkg: Pkg
Pkg.activate(@__DIR__)
Pkg.instantiate()

using JuMP
using GLPK
using Random

file = ""       # Instances file name
seed = 0        # Random seed from user input
time_limit = 0
n = 0           # Number of instances
capacity = 0    # Max capacity of the TKP

# Checks for required three additional arguments
try
    global file = ARGS[1]
    global seed = parse(Int, ARGS[2])
    global time_limit = parse(Int, ARGS[3])
catch e
    println("ERROR: Exactly three arguments are required.\nUsage: julia tkp.jl instance_file random_seed time_limit.\n")
    exit(1)
end

# Reads the instances and creates the price, demand and intervals arrays
try
    println("Opening from $file...\n")
    open(file) do f
        # First and second lines from the file are the size and max capacity respectively
        global n = parse(Int, readline(f))
		global capacity = parse(Int, readline(f))
        
        item_count = 0

        # TODO: create an array of int instead of floats
        global price = zeros(n)
        global demand = zeros(n)
        global start = zeros(n)
        global finish = zeros(n)

        # Parse throw the instances
        while (item_count < n)
            line = readline(f)
            temp = split(line, " ") 
            # The last element from the split array is an empty string
            pop!(temp)                  
            # Array of strings to array of ints
            item = [parse(Int, x) for x in temp]

            # Fill the arrays
            price[item_count+1] = item[1]
            demand[item_count+1] = item[2]
            start[item_count+1] = item[3]
            finish[item_count+1] = item[4]

            item_count += 1
        end
    end
catch e
    println("ERROR: Error finding or reading the file.\n")
    exit(1)
end

max_time = maximum(finish)

Random.seed!(seed)

# Solver implementation
model = Model(GLPK.Optimizer)
set_time_limit_sec(model, time_limit)
# Binary variable representing if item i is in the solution
@variable(model, x[1:n], Bin)
# Objective function
@objective(model, Max, sum(price[i]*x[i] for i in 1:n))

# Constraints
for t in 1:max_time
    for i in 1:n
        
    end
end

optimize!(model)