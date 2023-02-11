# Weasel program
# Lev Bernstein


from math import log
from random import choice, randint


PHRASE = "METHINKS IT IS LIKE A WEASEL"
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
MAX_GENERATIONS = 10000
MUTATION_RATE = 5


def mutate() -> bool:
	return randint(1, 100) <= MUTATION_RATE


def fitness(survivor: str, target: str) -> int:
	if len(survivor) != len(target):
		raise Exception("Strings must be the same length!")
	return sum((int(survivor[i] == target[i]) for i in range(len(survivor))))


def strcmp(a: str, b: str, target: str) -> str:
	# Return string with higher fitness
	return a if fitness(a, target) > fitness(b, target) else b


def spawn(parent: str) -> str:
	return "".join(choice(LETTERS) if mutate() else letter for letter in parent)


def compete(parent: str, target: str, litter_size: int) -> str:
	# Spawn a litter of children, return the one with the highest fitness
	# Performance could probably be improved via use of a heap; however, I/O
	# is the biggest performance bottleneck, so not significant
	child = spawn(parent)
	for i in range(litter_size - 1):
		child = strcmp(child, spawn(parent), target)
	return strcmp(parent, child, target)


if __name__ == "__main__":
	seed = "".join(choice(LETTERS) for i in range(len(PHRASE)))
	for j in (1, 2, 5, 10, 20, 50, 100):
		survivor = seed
		print(f"\n{j}-child version:\nGeneration      Child         Score")
		print(0, survivor, fitness(survivor, PHRASE))
		for i in range(1, MAX_GENERATIONS + 1):
			survivor = compete(survivor, PHRASE, j)
			if PHRASE == survivor:
				print(i, survivor, fitness(survivor, PHRASE))
				print(f"{j}-child program successful on generation {i}.")
				break
			if i % int(4 * (1 + (log(2 * MAX_GENERATIONS, 1.05 ** j)))) == 0:
				print(i, survivor, fitness(survivor, PHRASE))
