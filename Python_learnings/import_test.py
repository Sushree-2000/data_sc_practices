# import blackjack
# # print(__name__)

# # blackjack.deal_card(blackjack.dealer_card_frame)
# # blackjack.play()

# personal_details = ("Subha", 30, "Data Scientist")
# name, _, country = personal_details
# print(name)


# from blackjack import *

# g = sorted(globals())
# for x in g:
#     print(x)

# deal_card(dealer_card_frame)




# recursion
def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n-1) + fib(n-2)
    
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

for i in range(10):
    print(fib(i), end=' ')
# print(fib(10))
# print(fibonacci(10))