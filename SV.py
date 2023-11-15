import pygame
import random
import math

pygame.init()

class DrawInformation:

	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	GREEN = 0, 255, 0
	RED = 255, 0, 0
	BACKGROUND_COLOR = WHITE

	GRADIENTS = [
		(128, 128, 128),
		(160, 160, 160),
		(192,192,192)
	]

	FONT = pygame.font.SysFont('comicsans', 20)
	LARGE_FONT = pygame.font.SysFont('comicsans', 30)

	SIDE_PAD = 100 #Padding from Edges
	TOP_PAD = 150  #Padding from Top

	def __init__(self, width, height, lst):

		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Sorting Visualizer")

		self.set_list(lst)



	def set_list(self, lst):
		self.lst = lst
		self.max_val = max(lst)
		self.min_val = min(lst)


		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
		self.start_x = self.SIDE_PAD // 2

#End Class ----------------------------------------------------------------------------------------


def draw(draw_info, algo_name, ascending):
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)

	title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5)) #Blit allows to put a surface on another one


	controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45)) #Blit allows to put a surface on another one


	sorting = draw_info.FONT.render("Q - Quicksort | B - Bubble Sort | H - Heapsort | M - Mergesort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75)) #Blit allows to put a surface on another one


	draw_list(draw_info)
	pygame.display.update()



def draw_list(draw_info, color_positions={}, clear_bg = False):

	lst = draw_info.lst

	if clear_bg: #It's used to fill the background wityh white after each swap made by the sort algorithm
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
			draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(lst):
		x = draw_info.start_x + i*draw_info.block_width
		y = draw_info.height - ((val - draw_info.min_val) * draw_info.block_height)

		color = draw_info.GRADIENTS[i % 3]

		if(i in color_positions):
			color = color_positions[i]

		#Actually draw:
		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height)) #fix this with right parameters: draw_info.block_height*val

	if clear_bg: #If clear bg is true it means that we called this function from sort algorithm and we need to update
		pygame.display.update()


def generate_starting_list(n, min_val, max_val):
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val)
		lst.append(val)

	return lst



#------------------------------------------------------------------------------------------------

def BUBBLE_SORT(draw_info, ascending = True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if((num1 > num2 and ascending) or (num1 < num2 and not ascending)):
				lst[j], lst[j+1] = lst[j+1], lst[j]
				draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
				yield True #It's used to check if you finished to sort (Line 141)
									

	return lst

#------------------------------------------------------------------------------------------------


def QUICKSORT(draw_info, ascending = True):

	arr = draw_info.lst
	stack = [(0, len(arr) - 1)]

	while stack:
		low, high = stack.pop()
		if low < high:

			pivot = arr[high]
			i = low - 1
			for j in range(low, high):
				if ((arr[j] <= pivot and ascending) or (arr[j] > pivot and not ascending)):
					i += 1
					arr[i], arr[j] = arr[j], arr[i]
					draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
					yield True #It's used to check if you finished to sort (Line 141)

			arr[i + 1], arr[high] = arr[high], arr[i + 1]

			stack.append((low, i))
			stack.append((i + 2, high))


#------------------------------------------------------------------------------------------------

def HEAP_SORT(draw_info, ascending):

	arr = draw_info.lst
	n = len(arr)

	for i in range(n // 2 - 1, -1, -1):
		current = i
		while current < n:
			left_child = 2 * current + 1
			right_child = 2 * current + 2
			largest = current

			if left_child < n and ((arr[left_child] > arr[largest] and ascending) or (arr[left_child] <= arr[largest] and not ascending)):
			    largest = left_child

			if right_child < n and ((arr[right_child] > arr[largest] and ascending) or (arr[right_child] <= arr[largest] and not ascending)):
			    largest = right_child

			if largest != current:
				arr[current], arr[largest] = arr[largest], arr[current]
				draw_list(draw_info, {current: draw_info.GREEN, largest: draw_info.RED}, True)
				yield True #It's used to check if you finished to sort (Line 141)
				current = largest
			else:
			    break

	# Extract elements from the heap one by one
	for i in range(n - 1, 0, -1):
		arr[0], arr[i] = arr[i], arr[0]  # Swap the root (max element) with the last element
		current = 0
		while current < i:
			left_child = 2 * current + 1
			right_child = 2 * current + 2
			largest = current

			if left_child < i and ((arr[left_child] > arr[largest] and ascending) or (arr[left_child] <= arr[largest] and not ascending)):
			    largest = left_child

			if right_child < i and ((arr[right_child] > arr[largest] and ascending) or (arr[right_child] <= arr[largest] and not ascending)):
			    largest = right_child

			if largest != current:
				arr[current], arr[largest] = arr[largest], arr[current]
				draw_list(draw_info, {current: draw_info.GREEN, largest: draw_info.RED}, True)
				yield True #It's used to check if you finished to sort (Line 141)
				current = largest
			else:
			    break


#------------------------------------------------------------------------------------------------


def MERGESORT(draw_info, ascending):

	arr = draw_info.lst
	n = len(arr)
	current_size = 1

	while current_size < n:
		left = 0

		while left < n - 1:

			mid = min(left + current_size - 1, n - 1)
			right = min(left + 2 * current_size - 1, n - 1)

			merged = []
			i, j = left, mid + 1

			while i <= mid and j <= right:
				if ((arr[i] <= arr[j] and ascending) or (arr[i] > arr[j] and not ascending)):
				    merged.append(arr[i])
				    i += 1
				else:
				    merged.append(arr[j])
				    j += 1

				draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
				yield True #It's used to check if you finished to sort (Line 141)

			while i <= mid:
			    merged.append(arr[i])
			    i += 1

			while j <= right:
			    merged.append(arr[j])
			    j += 1

			# Copy the merged array back to the original array
			for k in range(len(merged)):
				arr[left + k] = merged[k]

			left += 2 * current_size

		current_size *= 2


#------------------------------------------------------------------------------------------------

def main():

	n = 100
	min_val = 0
	max_val = 100
	lst = generate_starting_list(n, min_val, max_val)
	draw_info = DrawInformation(1000, 800, lst)


	sorting = False
	ascending = True

	sorting_algorithm = BUBBLE_SORT #store function used to sort
	sorting_algo_name = "Bubble Sort"
	sorting_algorithm_generator = None

	run = True #In Pygame you need an infinite Loop
	clock = pygame.time.Clock()

	while run:
		clock.tick(60) #Maximum time loop can be executed per second

		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = False
		else:
			draw(draw_info, sorting_algo_name, ascending)


		for event in pygame.event.get(): #Return all events happend
			if(event.type == pygame.QUIT): #The red X on the bottom right side 
				run = False

			if(event.type != pygame.KEYDOWN):
				continue

			if(event.key == pygame.K_r): #when you press 'r'
				lst = generate_starting_list(n, min_val, max_val)
				draw_info.set_list(lst)
				draw(draw_info, sorting_algo_name, ascending)
				sorting = False
			elif(event.key == pygame.K_SPACE and sorting == False): #when you press 'SPACE'
				sorting = True
				sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

			elif(event.key == pygame.K_b and not sorting): #when you press 'b'
				sorting_algorithm = BUBBLE_SORT #store function used to sort
				sorting_algo_name = "Bubble Sort"

			elif(event.key == pygame.K_q and not sorting): #when you press 'q'
				sorting_algorithm = QUICKSORT #store function used to sort
				sorting_algo_name = "Quicksort"

			elif(event.key == pygame.K_h and not sorting): #when you press 'h'
				sorting_algorithm = HEAP_SORT #store function used to sort
				sorting_algo_name = "Heapsort"

			elif(event.key == pygame.K_m and not sorting): #when you press 'm'
				sorting_algorithm = MERGESORT #store function used to sort
				sorting_algo_name = "Mergesort"

			elif(event.key == pygame.K_a and not sorting): #when you press 'a'
				ascending = True

			elif(event.key == pygame.K_d and not sorting): #when you press 'd'
				ascending = False


	pygame.quit()



if __name__ == "__main__":
	main()



