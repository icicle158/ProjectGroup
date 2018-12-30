--Credit and Acknowledgements given to SethBling for some ideas,
--inspiration, and structure in creating my own version of his idea. 
--Thank you, Seth.


press_right_table = {}
press_right = function()
  if joypad.get()["P1 A"] then
    press_right_table["P1 Right"] = true
    joypad.set(press_right_table)
  end
end


cell_grid = true

--CAN BE SET FOR 1 or 2 depending on which memory address has
--the current tiles mario is standing on
x_screen_pos_flag = 1
function create_rectangle()
  
  screen_height = client.screenheight()
  screen_width = client.screenwidth()
  
  
  --Relating to Mario's position & screen offset
  ----------------------------------------------------------------------------
  --Mario's level x-position
  x_level = mainmemory.readbyte(0x006D)
  --Mario's x-position on screen (relative to player)
  x_screen = mainmemory.readbyte(0x0086)
  
  --This is dividing the screens by 16 to display each
  --tile position
  x_screen_pos = (x_screen - x_screen % 16)/16
  
  --So, Original super mario bros keeps track of the level
  --generation through the use of thirty-two memory addresses
  --Each address contains a value for what type of tile it is.
  --This is used to denote which sub-memory address contains
  --the current tiles mario is looking at. 2 sub memory addresses
  --each containing 16 memory addresses. 32 in total.
  if (x_level % 2) == 1 then
    x_screen_pos_flag = 2
  else
    x_screen_pos_flag = 1
  end
    
  if x_screen_pos_flag == 2 then
    x_screen_pos = x_screen_pos + 16
    if x_screen_pos == 31 then
      x_screen_pos_flag = 1
    end
  end

  --Used to look at the offset (in tiles) mario is away from the screen
  curr_tile_screenoff = mainmemory.readbyte(0x03AD)
  curr_t_screenoff_scale = (curr_tile_screenoff - curr_tile_screenoff % 16)/16
  
  if (x_screen_pos - curr_t_screenoff_scale) < 0 then
    range_i = 31 + (x_screen_pos - curr_t_screenoff_scale)
    if range_i > 31 then
      range_i = range_i - 31
    end
      
  else
    range_i = x_screen_pos - curr_t_screenoff_scale
    if range_i > 31 then
      range_i = range_i - 31
    end
  end
  ----------------------------------------------------------------------------
  
  --Draws the screen for the "eyeball"
  gui.drawBox(10, 40, (screen_width / 8) + 10, (screen_height / 8) + 40, "black", "gray")
  
  
    --TESTING--
  all_tiles = mainmemory.readbyterange(0x04FF, 417)
  all_tile_table = {}
  temp_table = {}
  z = 0
  key_i = 0
  all_iter = 0
  layer_switch = false
 
  for k,v in pairs(all_tiles) do
    
    if layer_switch == false then
      if (z % 16 == 0) and (z ~= 0) then
        all_tile_table[tonumber(all_iter)] = temp_table
        temp_table = {}
        key_i = 0
        all_iter = all_iter + 1
      end
    end
    
    if z == 208 then
      layer_switch = true
      all_iter = 0
    end
    
    if layer_switch == true then
      if (z % 16 == 0) and (z ~= 208) then
        all_iter = all_iter + 1
        key_i = 0
      end
      
      if z < 417 and all_iter ~= 13 then
        all_tile_table[tonumber(all_iter)][16+key_i] = v
      end
    end
      
    temp_table[tonumber(key_i)] = v
    z = z + 1
    key_i = key_i + 1
  end
  --TESTING--
  
  --MUST READ FROM MORE THAN 0x05B0
  --Must also read from 0x0680 & 0x0690
  ground_field_1 = mainmemory.readbyterange(0x05B0, 17)
  ground_field_2 = mainmemory.readbyterange(0x0680, 17)
  
  ground_field_3 = mainmemory.readbyterange(0x05C0, 17)
  ground_field_4 = mainmemory.readbyterange(0x0690, 17)
  
  
  
  --Take all of the ground tiles currently being loaded into memory
  --and add them into one table
  for k,v in pairs(ground_field_2) do
    ground_field_1[k+table.getn(ground_field_2)] = v
  end
  
  for k,v in pairs(ground_field_4) do
    ground_field_3[k+table.getn(ground_field_4)] = v
  end
  
  ground_field = ground_field_1
  ground_field_layer2 = ground_field_3


  --This value is assigned due to 16 tiles on screen
  --Change later to make it more versatile (TESTING ONLY)
  decrement_value_width = (((screen_width / 8)))/16
  
  height_range = (screen_height / 8) / 13
  
  i = 0
  
  --Table used to map iterators correctly
  --Used on the inner while loop (ex: while i < 11)
  h_table = {}
  air_tile_copy = {}
  while i < 17 do
    
    if range_i == 32 then
        range_i = 0
    end
    
    ------//////Block of code for tiles in air//////
    iter = 0
    height_mult = 12
    l1 = 0
    s_draw_l1 = 10
    
    while iter < 13 do
      
      if h_table[height_mult] == nil then
        h_table[height_mult] = 0
      end
      
      s_edraw_l1 = (10 + h_table[height_mult])
      
      --if air_tiles[iter][range_i] > 0x0000 then
      if all_tile_table[iter][range_i] > 0x0000 then
        gui.drawBox(s_draw_l1, (screen_height / 8) + (40 - height_range*height_mult), s_edraw_l1, ((screen_height / 8) + (40 - height_range*height_mult)) - height_range)
        air_tile_copy[height_mult] = s_edraw_l1
        h_table[height_mult] = (h_table[height_mult] + decrement_value_width)
      end
            
      --if air_tiles[iter][range_i] == 0x0000 then
      if all_tile_table[iter][range_i] == 0x0000 then
        air_tile_copy[height_mult] = s_edraw_l1
        h_table[height_mult] = (h_table[height_mult] + decrement_value_width)
      end
      iter = iter + 1
      height_mult = height_mult - 1
      
      if air_tile_copy[height_mult] ~= nil then
        s_draw_l1 = air_tile_copy[height_mult]
      end
    end
  ------//////End Block//////
  
    
    i = i + 1
    range_i = range_i + 1
  end
end


--This function is used to generate a table containing a list
--of all visibile 'standable' tiles in the game (not enemy tiles or mario).
--The table has a mapping with the key representing the tile number from left
--to right starting at 0 and ending at (16*13)-1 (# width tiles * # height tiles)
--with a value of -1 if mario can't stand on the tile and a value of 1 if mario can.
function generate_visual_inputs()
  
  --Used to capture all input neurons
  local input_neurons = {}
  
  
  screen_height = client.screenheight()
  screen_width = client.screenwidth()
  
  x_level = mainmemory.readbyte(0x006D)
  x_screen = mainmemory.readbyte(0x0086)
  
  x_screen_pos = (x_screen - x_screen % 16)/16
  
  if (x_level % 2) == 1 then
    x_screen_pos_flag = 2
  else
    x_screen_pos_flag = 1
  end
    
  if x_screen_pos_flag == 2 then
    x_screen_pos = x_screen_pos + 16
    if x_screen_pos == 31 then
      x_screen_pos_flag = 1
    end
  end
  
  curr_tile_screenoff = mainmemory.readbyte(0x03AD)
  curr_t_screenoff_scale = (curr_tile_screenoff - curr_tile_screenoff % 16)/16
  
  if (x_screen_pos - curr_t_screenoff_scale) < 0 then
    range_i = 31 + (x_screen_pos - curr_t_screenoff_scale)
    if range_i > 31 then
      range_i = range_i - 31
    end
      
  else
    range_i = x_screen_pos - curr_t_screenoff_scale
    if range_i > 31 then
      range_i = range_i - 31
    end
  end
  

  all_tiles = mainmemory.readbyterange(0x04FF, 417)
  all_tile_table = {}
  temp_table = {}
  z = 0
  key_i = 0
  all_iter = 0
  layer_switch = false
 
  for k,v in pairs(all_tiles) do
    
    if layer_switch == false then
      if (z % 16 == 0) and (z ~= 0) then
        all_tile_table[tonumber(all_iter)] = temp_table
        temp_table = {}
        key_i = 0
        all_iter = all_iter + 1
      end
    end
    
    if z == 208 then
      layer_switch = true
      all_iter = 0
    end
    
    if layer_switch == true then
      if (z % 16 == 0) and (z ~= 208) then
        all_iter = all_iter + 1
        key_i = 0
      end
      
      if z < 417 and all_iter ~= 13 then
        all_tile_table[tonumber(all_iter)][16+key_i] = v
      end
    end
      
    temp_table[tonumber(key_i)] = v
    z = z + 1
    key_i = key_i + 1
  end
  
  
  tile_num = 1
  i = 0
  while i < 16 do
    
    if range_i == 32 then
        range_i = 0
    end
    
    iter = 0
    while iter < 13 do
    
      if all_tile_table[iter][range_i] > 0x0000 then
        input_neurons[tile_num] = 1
      end
            
      if all_tile_table[iter][range_i] == 0x0000 then
        input_neurons[tile_num] = -1
      end
      
      iter = iter + 1
      --height_mult = height_mult - 1
      tile_num = tile_num + 1
    end
    
    i = i + 1
    range_i = range_i + 1
  end
  
  
  return input_neurons
end


function view_cell_grid()
  
  screen_height = client.screenheight()
  screen_width = client.screenwidth()
  
  cell_height = 256 / 16
  cell_width = 256 / 16
  
  i = 0
  while i < 16 do
    gui.drawLine(0, (cell_height * i), screen_width, (cell_height * i), "gray")
    gui.drawLine((cell_width * i), 0, (cell_width * i), screen_height, "gray")
    i = i + 1
  end
end


--//Relating to NEAT (Neural Evolution of Augmenting Toplogies)

--/////NOTES//////
--Select individual cells (once the network is working) to distribute
--Individual nodes to each cell position. Once an alteration/conflict
--occurs at the watched cell, the node is activated (or not! Depending
--on if the node is disabled or not)

--PLEASE REMEMBER: When using '#' to find the length of a list, increment that
--number by 1. '#' returns the last indexed key (which is 1 from the total size)


--ULTRA IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
--ALL ITERATIONS IN LUA ARE DONE STARTING AT INDEX: 1
--This is due to the stupidity of lua engineers


--Random neurons when generated through a random mutation chance, have an
--index that is incremented onto the current max index of the input nodes
--With a maximum of 208 nodes, (Node:0 - Node:207) Node 208 represents the
--first randomly generated node. Followed by 209, 210... etc.


--Different types of mutation rates such as:
--1.) Link mutation
--2.) Node mutation
--3.) Gene mutation


--Initializers

--Number of tiles on screen
input_nodes = 16*13
--A, B, Up, Down, Left, Right
output_nodes = 6

--Cap the maximum node count to 10,000,000 nodes
max_nodes = 10000000

population_size = 100


--1.0 represents a 100% chance to mutate
link_mutation_chance = 1.0

hiddenlayer_node_chance = 1.0


--Total gene innovation number
--Start at 0, and before a gene_innovation is assigned, increment the global value.
--This way, gene innovation numbers are assigned accurately
gene_innovation = 0



button_table = {
  
[1+max_nodes] = {["P1 A"] = true},
[2+max_nodes] = {["P1 B"] = true},
[3+max_nodes] = {["P1 Right"] = true},
[4+max_nodes] = {["P1 Up"] = true},
[5+max_nodes] = {["P1 Down"] = true},
[6+max_nodes] = {["P1 Left"] = true}

}
  
--Genes are held within nodes. They represent the mapping
--from one node to another (from one gene to another)
function create_gene(hist_mark)
  local gene = {}
  gene.innovation = 0
  gene.out_conn = 0
  gene.in_conn = 0
  gene.weight = 0.0
  gene.enabled = true
  
  return gene
end

function create_neuron()
  local neuron = {}
  
  --May be useful
  --neuron.id = 0
  
  --This correlates the gene-number entering the node to the node-number.
  --different genes may enter different nodes. Node 1 may have Gene2, Gene3, & Gene7
  --as an example
  neuron.gene_map = {}
  neuron.activation = 0.0
  
  return neuron
end
  
--Terminology for genome (Phenotype)
--Perhaps add a parameter to specify the new historical number of a phenotype
function create_phenotype()
  local phenotype = {}
  phenotype.genes = {}
  phenotype.neural_net = {}
  phenotype.historical_mark = 1
  phenotype.fitness_rank = 0
  phenotype.mutation_rates = {}
  
  --Represents the current index number of any randomly generated
  --neurons within a phenotype
  --We start at 0 with this particular value to represent a neuron
  --has been added. Yes, this will make iteration slightly more tough.
  phenotype.random_neuron_index = 0
  
  return phenotype
end


--The initial phenotype takes the kingdom as a parameter to use later
--for gene cataloging
function initial_phenotype(kingdom)
  first_phenotype = create_phenotype()
  --!!!!May need to change this!!!!--
  first_phenotype.historical_mark = 1
  
  --Should be placed AFTER genes are inserted into network to account
  --for any neurons that should be added due to the addition of a gene
  create_network(first_phenotype)
  mutate(first_phenotype, kingdom)
  
  
  --USED FOR TESTING--
  count_phenotype_genes(first_phenotype)
  
  
  
  return first_phenotype
end

function create_species()
  local species = {}
  species.species_number = 0
  species.phenotypes = {}
  
  
  
  --This value represents the threshold with which two phenotypes
  --are merged into a species. This value is used in tandem with 
  --the measure speciation function
  --This value is experimental. Use it to change the rate at which species
  --are developed
  species.speciation_threshold = 2.0
  
  return species
end

function create_kingdom()
  local kingdom = {}
  kingdom.species = {}
  kingdom.total_genes = {}
  kingdom.innovation = 1
  
  return kingdom
end


--Generates a network for an input phenotype
function create_network(phenotype)
  local neural_net = {}

  
  for i=1, input_nodes do
    neural_net[i] = create_neuron()
  end
  
  
  --Run an additional loop to generate any additional nodes which
  --are created by genes *IMPORTANT*
  
  
  for i=1, output_nodes do
    neural_net[max_nodes+i] = create_neuron()
  end
  
  
  phenotype.neural_net = neural_net
end


--This function is called after the network is executed (performed).
--this function will go through and re-evaluate all of the neurons activation
--values according to the sigmoid function
function reinforce_network(phenotype)
  
  --This contains a table of all input values. 1 represents a block mario
  --can stand on, while -1 represents no block.
  input_table = generate_visual_inputs()
  
  
  --SORTING MAY BE NECESSARY
  --table.sort(phenotype.neural_net)
  
  
  --This should update only the first 208 input nodes
  for i=1, input_nodes do
    phenotype.neural_net[i].activation = input_table[i]
  end
  
  
  --This value is used to calculate the addition of the activation
  --value of a neuron multiplied by the weights of all genes within the
  --the neuron's incoming gene list
  new_activation = 0
  has_gene_map = false
  for k,v in pairs(phenotype.neural_net) do
    --print(k, v)
    for key,gene in pairs(phenotype.neural_net[k].gene_map) do
      --print(key, gene)
      new_activation = new_activation + (phenotype.neural_net[k].activation * gene.weight)
      has_gene_map = true
    end
    if has_gene_map == true then
      phenotype.neural_net[k].activation = sigmoid(new_activation)
    end
    has_gene_map = false
  end
  

  --This table will contain a list of all the values the controller should press
  --after evaluation of the summation of the weights and activation values of the
  --genes and nodes respectively
  
  --Using out_cnt to create a new table index is more efficient for calling the
  --values later on (for the joypad). As opposed to using the (max_nodes + j) which
  --would not index all of the button outputs due to the 'if' statement
  out_cnt = 1
  output_values = {}
  for j=1, output_nodes do
    if phenotype.neural_net[j+max_nodes].activation > 0 then
      output_values[out_cnt] = button_table[j+max_nodes]
      out_cnt = out_cnt + 1
    end
  end
    
  return output_values
  --Now we want to go through our network and select an output based off of
  --our input value
    
end


--This function generates the first link between an input
--node and an output node within a given phenotype
--The in_out_flag represents if we're looking for an input
--node or an output node (true == input) (false == output)
function generate_first_link(phenotype, in_out_flag)
  
  local neurons = {}
  
  if in_out_flag == true then
    for i=1, input_nodes do
      --Set the neurons to their respective index value for easy
      --indexing
      neurons[i] = i
    end
  end
  
  if in_out_flag == false then
    for i=1, output_nodes do
      neurons[i] = (i + max_nodes)
    end
  end
  
  neuron_count = 0
  for k,v in pairs(neurons) do
    neuron_count = neuron_count + 1
  end
  
  rand_neuron = math.random(1, neuron_count)
  
  return neurons[rand_neuron]
end


--This function is called when the phenotype has genes already
--present within its network. If genes exist, this function is able
--to correctly generate new random links between not only the input
--nodes and output nodes but nodes within the hidden layer as well.
--Nodes within the hidden layer are considered "input" nodes for this
--particular context.
----------------------------------------------------------------------
--Initially, we run through the network and pick
--an input and an output neuron to link.
--The in_out_flag represents whether the neuron
--being selected needs to be an input or an output
--node. When the program initially starts, the first
--generated phenotypes have no connections between the
--input and output nodes. Thus, this flag ensures that
--the first two selected nodes are an input and an output, respectively.
function generate_additional_links(phenotype, in_out_flag)
  
  local neurons = {}
  
  if in_out_flag == true then
    for i=1, (input_nodes+phenotype.random_neuron_index) do
      neurons[i] = i
    end
  end
  
  --Because an input node can now connect to hidden layer nodes, the output
  --node is harder to calculate. Inputs can connect to hidden layer or outputs.
  --Similarly, hidden layer can connect to other hidden layer and outputs. Thus,
  --I have installed some checks to determine by chance whether the next output
  --node is either a hidden layer node or an output node
  if phenotype.random_neuron_index > 2 then
    hidden_or_output_check = phenotype.random_neuron_index + output_nodes
    decision_maker = math.random(1, hidden_or_output_check)
  else
    --Make the decision maker 1 greater than to phenotype random neuron count (index)
    --in order to trigger the second if statement and force an output neuron to be
    --selected between
    decision_maker = phenotype.random_neuron_index + 1
  end
  
  
  if decision_maker <= phenotype.random_neuron_index then
    if in_out_flag == false then
      for i=1, phenotype.random_neuron_index do
        neurons[i] = (input_nodes + i)
      end
    end
  end
  
  if decision_maker > phenotype.random_neuron_index then
    if in_out_flag == false then
      for i=1, output_nodes do
        neurons[i] = (i + max_nodes)
      end
    end
  end
      
      
  neuron_count = 0
  for k,v in pairs(neurons) do
    neuron_count = neuron_count + 1
  end
  
  rand_neuron = math.random(1, neuron_count)
  
  return neurons[rand_neuron]
  
end


--Nodes randomly generated to process inputs and generate responses to either:
--1.) Other hidden layer nodes 2.) Output layer nodes
function mutateinto_hiddenlayer_node(phenotype, kingdom)
  
  new_neuron = create_neuron()
  
  
  --This table will be used to hold a random gene's information
  rand_gene_table = {}
  
  gene_count = 0
  
  for k,v in pairs(phenotype.neural_net) do
    for key, val in pairs(phenotype.neural_net[k].gene_map) do
      gene_count = gene_count + 1
    end
  end
  
  
  --DOES NOT TEST IF THERE ARE LESS THAN 1 GENES IN THE PHENOTYPE
  if gene_count == 1 then
    rand_gene = 1
  else
    rand_gene = math.random(1, gene_count)
  end
  
  
  for k,v in pairs(phenotype.neural_net) do
    for key, val in pairs(phenotype.neural_net[k].gene_map) do
      rand_gene = rand_gene - 1
      if (rand_gene == 0) then
        --Right here, we disable the originally constructed gene. This represents
        --that is has been split by a node into two, separately unique, genes.
        
        
        --WORK ON MODIFYING CODE TO SUPPORT GENES BEING ENABLED AND DISABLED!!!!!!!
        phenotype.neural_net[k].gene_map[key].enabled = false
        rand_gene_table[1] = val
        break
      end
    end
  end
  
  --Create 2 new genes for each new link
  new_gene1 = create_gene()
  
  new_gene1.in_conn = rand_gene_table[1]["in_conn"]
  phenotype.random_neuron_index = phenotype.random_neuron_index + 1
  new_gene1.out_conn = input_nodes + phenotype.random_neuron_index
  new_gene1.weight = math.random() * 2
  
  new_neuron.gene_map[new_gene1.innovation] = new_gene1
  
  new_gene2 = create_gene()
  
  new_gene2.in_conn = new_gene1.out_conn
  new_gene2.out_conn = rand_gene_table[1]["out_conn"]
  new_gene2.weight = math.random() * 2
  
  
  --total gene count
  --WORK ON THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!--
  t_gene_cnt = 0
  --for k,v in pairs(kingdom.total_genes) do
  --  t_gene_cnt = t_gene_cnt + 1
  --end
  
  if t_gene_cnt == 0 then
    gene_innovation = gene_innovation + 1
    new_gene1.innovation = gene_innovation
    --IMPORTANT
    --kingdom.total_genes[new_gene1.innovation] = new_gene1
    
    gene_innovation = gene_innovation + 1
    new_gene2.innovation = gene_innovation
    --IMPORTANT
    --kingdom.total_genes[new_gene2.innovation] = new_gene2
    
    phenotype.genes[new_gene1.innovation] = new_gene1
    phenotype.genes[new_gene2.innovation] = new_gene2
    phenotype.neural_net[rand_gene_table[1]["out_conn"]].gene_map[new_gene2.innovation] = new_gene2
    phenotype.neural_net[input_nodes + phenotype.random_neuron_index] = new_neuron
    
    --Work on this next
  --else
    --for k,v in pairs(kingdom.total_genes) do
      --if (v.in_conn == new_gene1.in_conn) and (v.out_conn == new_gene1.out_conn) then
  
  end
  
  --keep neuron activation value at zero upon creation. More testing with this
  --can be done later
  
  --BE SURE TO USE ENABLED GENE FALSE!
  
  --Successfully captured a random gene. Now, disable that gene, and split the
  --connection whilst adding a neuron between the original in/out neurons
  for k,v in pairs(phenotype.neural_net) do
    print(k, "--------New Neuron--------")
    for key, val in pairs(phenotype.neural_net[k].gene_map) do
    --new_neuron.gene_map
    print(key, val)
    end
  end
      
      
end


function sigmoid(activation_value)
  sigmoid_val = 1/(1+math.pow(2.718281828459,(-4.9 * activation_value)))
  return sigmoid_val
end


function link_mutation(phenotype, kingdom)
  
  gene_count = 0
  for k,v in pairs(phenotype.genes) do
    gene_count = gene_count + 1
  end
  
  if gene_count == 0 then
    first_neuron = generate_first_link(phenotype, true)
    second_neuron = generate_first_link(phenotype, false)
    
    --Sanity checks to ensure that the first node is an input node
    --and the second node is an output node
    if first_neuron > input_nodes then
      print("First node is not an input node")
      return
    end
    if second_neuron <= input_nodes then
      print("Second node is not an output node")
    end
    
    new_gene = create_gene()
    gene_innovation = gene_innovation + 1
    new_gene.innovation = gene_innovation
    new_gene.in_conn = first_neuron
    new_gene.out_conn = second_neuron
    new_gene.weight = math.random() * 2
    
    phenotype.genes[new_gene.innovation] = new_gene
    phenotype.neural_net[second_neuron].gene_map[new_gene.innovation] = new_gene
    
  end
  
  
  --********************IMPORTANT*************************
  --CAN ONLY TEST THE FUNCTIONALITY OF THIS UPON AT LEAST 1 NETWORK REINFORCEMENT
  --DUE TO STARTING WITH 0 GENES INITIALLY
  if gene_count > 0 then
    first_neuron = generate_additional_links(phenotype, true)
    second_neuron = generate_additional_links(phenotype, false)
    
    
    --Sanity checks to ensure that the first node is an input node
    --or a hidden layer node and the second node is either a hidden
    --layer node or an output node
    if first_neuron > input_nodes then
      print("First node is not an input node or hidden layer node")
      return
    end
    if second_neuron <= input_nodes then
      print("Second node is not an output node or hidden layer node")
    end
    
    new_gene = create_gene()
    gene_innovation = gene_innovation + 1
    new_gene.innovation = gene_innovation
    new_gene.in_conn = first_neuron
    new_gene.out_conn = second_neuron
    new_gene.weight = math.random() * 2
    
    phenotype.genes[new_gene.innovation] = new_gene
    phenotype.neural_net[second_neuron].gene_map[new_gene.innovation] = new_gene
    
  end
end

function mutate(phenotype, kingdom)
  
  if link_mutation_chance == 1.0 then
    link_mutation(phenotype, kingdom)
  end
  
  if hiddenlayer_node_chance == 1.0 then
    mutateinto_hiddenlayer_node(phenotype, kingdom)
  end
    
end



function measure_speciation(phenotype1, phenotype2)
  disjoint_gene_pheno1 = 0
  excess_gene_pheno1 = 0
  
  disjoint_gene_pheno2 = 0
  excess_gene_pheno2 = 0
  
  total_genes_pheno1 = 0
  total_genes_pheno2 = 0
  
  
  for k,v in pairs(phenotype1.genes) do
    total_genes_pheno1 = total_genes_pheno1 + 1
  end
  
  for k,v in pairs(phenotype2.genes) do
    total_genes_pheno2 = total_genes_pheno2 + 1
  end
  
  --N represents the total genes of the phenotype with the most (or equal) genes
  N = 0
  if total_genes_pheno1 >= total_genes_pheno2 then
    N = total_genes_pheno1
  else
    N = total_genes_pheno2
  end
  
  
  --Some important realizations have been made:
  --1.) Ensure there is a way to denote similar genes between two networks. Check
  --to ensure the gene innovation number is being assigned and working correctly
  --for all phenotype networks. Thus, creating a universal log of gene innovation
  --numbers and their respective neuron associations would allow you to assign the
  --same gene innovation number to other networks (phenotypes) which support the same
  --neuron associations.
  --2.) Observe phenotype.genes when a new gene is assigned. Perform a check on all gene
  --associations currently available
    
  
  
  
end



--function add_phenotype_to_species()

--end

--function add_species_to_kingdom()

--end


-------FUNCTIONS FOR TESTING-----------------------------------------

--Used for testing
function count_phenotype_genes(phenotype)
  
  count_genes = 0
  for k,v in pairs(phenotype.genes) do
    count_genes = count_genes + 1
    print("Gene Key: ", k)
    print("Gene Value: ", v)
   -- print("DDDDDD")
  end
  
  --print("dd", count_genes)
  print("Gene Count: ", count_genes)
end
--------TESTING END---------------------------------------------------

kingdom = create_kingdom
output_vals = reinforce_network(initial_phenotype(kingdom))

while true do
  create_rectangle()
  
  
  --print(output_vals[1]["P1 A"])
  
  joypad.set(output_vals[1])
  
  
  --for k,v in pairs(reinforce_network(initial_phenotype())) do
  --  print(k,v)
  --end
  --joypad.set(reinforce_network(initial_phenotype()))
  

  --view_cell_grid()
  emu.frameadvance();
end

-----------IMPORTANT!--------------
--Functions below this point will be used for influencing emulator/system features (such as saving/loading/restarting a level)

function reset_level()
  --To do
end



