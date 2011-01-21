program Ga_Tutorial;

//	code to illustrate the use of a genetic algorithm to solve the problem described
//  at www.btinternet.com/~fup/ga_tutorial.htm
//
//	by Mat Buckland aka fupp
//  ported to Delphi by Asbjørn Heid aka Lord Crc

uses
  Windows,
  SysUtils;

{$APPTYPE CONSOLE}

const
  CROSSOVER_RATE = 0.7;
  MUTATION_RATE = 0.001;
  POP_SIZE = 40; //must be an even number
  CHROMO_LENGTH = 200;
  GENE_LENGTH = 4;
  MAX_ALLOWABLE_GENERATIONS = 200;

type
//	define a data structure which will define a chromosome
  TChromo = record
    bits: string;
    fitness: single;
  end;

//global storage for our population of chromosomes.
var
  g_Population: array[0..POP_SIZE-1] of TChromo;

// Initializes chromosone
function Chromo(bits: string = ''; fitness: single = 0): TChromo;
begin
  result.bits:= bits;
  result.fitness:= fitness;
end;

//	This function returns a string of random 1s and 0s of the desired length.
function GetRandomBits(length: integer): string;
var
  i: integer;
begin
  SetLength(result, length);

	for i:= 1 to length do
		if (random > 0.5) then
			result[i]:= '1'
		else
			result[i]:= '0';
end;

//	converts a binary string into a decimal integer
function BinToDec(bits: string): integer;
var
  i, value_to_add: integer;
begin
	result:= 0;
	value_to_add:= 1;

  for i:= length(bits) downto 1 do
  begin
    if bits[i] = '1' then
      result:= result + value_to_add;
    value_to_add:= value_to_add * 2;
  end;
end;

// Given a chromosome this function will step through the genes one at a time and insert
// the decimal values of each gene (which follow the operator - number - operator rule)
// into a buffer. Returns the number of elements in the buffer
function ParseBits(bits: string; var buffer: array of integer): integer;
var
  i, cBuff, this_gene: integer;
  bOperator: boolean;
begin
	//counter for buffer position
	cBuff:= 0;

	// step through bits a gene at a time until end and store decimal values
	// of valid operators and numbers. Don't forget we are looking for operator -
	// number - operator - number and so on... We ignore the unused genes 1111
	// and 1110

	//flag to determine if we are looking for an operator or a number
	bOperator:= true;

  i:= 1;
  while i <= CHROMO_LENGTH do
	begin
		//convert the current gene to decimal
		this_gene:= BinToDec(copy(bits, i, GENE_LENGTH));
		//find a gene which represents an operator
		if bOperator then
    begin
			if ( (this_gene >= 10) and (this_gene <= 13) ) then
      begin
				bOperator:= false;
				buffer[cBuff]:= this_gene;
        cBuff:= cBuff + 1;
			end;
		end
    else
		//find a gene which represents a number
    begin
			if (this_gene <= 9) then
      begin
				bOperator:= true;
				buffer[cBuff]:= this_gene;
        cBuff:= cBuff + 1;
      end;
		end;
    i:= i + GENE_LENGTH;
  end; // next gene

	//	now we have to run through buffer to see if a possible divide by zero
	//	is included and delete it. (ie a '/' followed by a '0'). We take an easy
	//	way out here and just change the '/' to a '+'. This will not effect the
	//	evolution of the solution

  for i:= 0 to cBuff-1 do
  begin
		if ( (buffer[i] = 13) and (buffer[i+1] = 0) ) then
			buffer[i]:= 10;
  end;

  result:= cBuff;
end;

//	given a string of bits and a target value this function will calculate its representation
//  and return a fitness score accordingly
function AssignFitness(bits: string; target_value: single): single;
var
	//holds decimal values of gene sequence
  buffer: array[0..(CHROMO_LENGTH div GENE_LENGTH)-1] of integer;
  i, num_elements: integer;
begin

	num_elements:= ParseBits(bits, buffer);

	// ok, we have a buffer filled with valid values of: operator - number - operator - number..
	// now we calculate what this represents.

	result:= 0;

  i:= 0;
  while i < num_elements-1 do
  begin
    case buffer[i] of
      10: result:= result + buffer[i+1];
      11: result:= result - buffer[i+1];
      12: result:= result * buffer[i+1];
      13: result:= result / buffer[i+1];
    end;

    i:= i + 2;
  end;

	// Now we calculate the fitness. First check to see if a solution has been found
	// and assign an arbitarily high fitness score if this is so.

	if (result = target_value) then
    result:= 999
	else
    result:= 1 / abs(target_value - result);
end;

//	given an integer this function outputs its meaning to the screen
procedure PrintGeneSymbol(val: integer);
begin
	if (val < 10 ) then
    write(val, ' ')
	else
  begin
    case val of
		  10: write('+');
		  11: write('-');
		  12: write('*');
		  13: write('/');
    end;
    write(' ');
  end;
end;

// decodes and prints a chromo to screen
procedure PrintChromo(bits: string);
var
  //holds decimal values of gene sequence
  buffer: array[0..(CHROMO_LENGTH div GENE_LENGTH)-1] of integer;
  i, num_elements: integer;
begin
	//parse the bit string
	num_elements:= ParseBits(bits, buffer);

	//now we have the buffer step through and print values
	writeln;
  writeln;

  for i:= 0 to num_elements-1 do
  begin
		PrintGeneSymbol(buffer[i]);
  end;

	writeln;
  writeln;
end;

//	Mutates a chromosomes bits dependent on the MUTATION_RATE
procedure Mutate(var bits: string);
var
  i: integer;
begin
  for i:= 1 to length(bits) do
  begin
    if (random < MUTATION_RATE) then
    begin
      if bits[i] = '1' then
        bits[i]:= '0'
      else
        bits[i]:= '1';
    end;
  end;
end;

//	selects a chromosome from the population via roulette wheel selection
function Roulette(total_fitness: single): string;
var
  Slice: single;
  FitnessSoFar: single;
  i: integer;
begin
  result:= '';

	//generate a random number between 0 & total fitness count
	Slice:= random * total_fitness;

	//go through the chromosones adding up the fitness so far
	FitnessSoFar:= 0;

  for i:= 0 to POP_SIZE-1 do
  begin
		FitnessSoFar:= FitnessSoFar + g_Population[i].fitness;

		//if the fitness so far > random number return the chromo at this point
		if (FitnessSoFar >= Slice) then
    begin
			result:= g_Population[i].bits;
      break;
    end;
  end;
end;

var
  Target, TotalFitness: single;
  i, GenerationsRequiredToFindASolution, cPop, crossover: integer;
	bFound: boolean;
  temp: array[0..POP_SIZE-1] of TChromo;
  bits1, bits2, t1, t2: string;
begin
	//seed the random number generator
  //Randomize;

	//get a target number from the user. (no error checking)
  Writeln;
  Write('Input a target number: ');
  ReadLn(Target);

	//first create a random population

  for i:= 0 to POP_SIZE-1 do
  begin
    g_Population[i]:= Chromo(GetRandomBits(CHROMO_LENGTH));
  end;

	GenerationsRequiredToFindASolution:= 0;

	//we will set this flag if a solution has been found
	bFound:= false;

  Writeln('Solutions found this run are: ');

	//enter the main GA loop
	while (not bFound) do
  begin
		//this is used during roulette wheel sampling
		TotalFitness:= 0;

		// test and update the fitness of the population.
		for i:= 0 to POP_SIZE-1 do
		begin
			g_Population[i].fitness:= AssignFitness(g_Population[i].bits, Target);

			TotalFitness:= TotalFitness + g_Population[i].fitness;
		end;

		// check to see if we have found any solutions (fitness will be 999)
		for i:= 0 to POP_SIZE-1 do
		begin
			if (g_Population[i].fitness = 999) then
			begin
				PrintChromo(g_Population[i].bits);

				bFound:= true;
			end;
		end;

		// create a new population by roulette wheel sampling of the
		// old population. Including crossover and mutation.

		cPop:= 0;

		//loop until we have created POP_SIZE new chromosomes
		while (cPop < POP_SIZE) do
		begin
			// we are going to create the new population by grabbing members of the old population
			// 2 at a time via roulette wheel selection.
			bits1:= Roulette(TotalFitness);
			bits2:= Roulette(TotalFitness);

			//now add crossover if required
			if (random < CROSSOVER_RATE) then
			begin
				//create a random crossover point
				crossover:= random(CHROMO_LENGTH)+1;

				t1:= copy(bits1, 1, crossover) + copy(bits2, crossover+1, CHROMO_LENGTH);
				t2:= copy(bits2, 1, crossover) + copy(bits1, crossover+1, CHROMO_LENGTH);

        assert(length(t1) = CHROMO_LENGTH);
        assert(length(t2) = CHROMO_LENGTH);

				bits1:= t1;
        bits2:= t2;
			end;

			//now mutate
			Mutate(bits1);
			Mutate(bits2);

			//now add to new population
			temp[cPop]:= Chromo(bits1);
      cPop:= cPop + 1;
			temp[cPop]:= Chromo(bits2);
      cPop:= cPop + 1;
		end; //end loop

		//copy temp population into main population array
		for i:= 0 to POP_SIZE-1 do
			g_Population[i]:= temp[i];

		GenerationsRequiredToFindASolution:= GenerationsRequiredToFindASolution + 1;

		// exit app if no solution found within tthe maximum allowable number
		// of generations
		if (GenerationsRequiredToFindASolution > MAX_ALLOWABLE_GENERATIONS) then
		begin
      writeln;
      writeln('No solutions found this run!');
			bFound:= true;
		end;
	end;

 
  writeln;
  writeln;
  writeln('Number of Generations required: ', GenerationsRequiredToFindASolution);
  writeln;
  writeln;
end.
