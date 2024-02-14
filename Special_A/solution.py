def solution(li):
    result = 1
    last = li[len(li)-1]
    for n in li:
        if n > last:
            result += 1
    return result

n = int(input(">"))

nums = [0]*n
for i in range(n):
    nums[i] = int(input(">>"))
    
result = solution(nums)
print(result)