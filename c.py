from typing import List, Any

nums1 = [12,24,8,32]
nums2 = [13,25,32,11]


length1 = len(nums1)
length2 = len(nums2)
ids: list[Any] = sorted(range(length1), key=lambda i: nums2[i])


print('x')
# for i in range(length1):
#
#     if nums1[i] > nums2[i]:
#         continue
#     if nu

nums = [10,20,40,5,10,50]


from collections import Counter

s1 = Counter(nums)
print(s1)
ans = t = 0

st = []
for i, v in enumerate(nums):
    if i == 0 or v > nums[i-1]:
        t += v
        ans = max(ans, t)
    else:
        t = v
print(ans)


n = 2
k = 10
a_length = 2**n
z = '0110'
print(a_length)
print(a_length % 4)
x = k % 4
print(x)


res = 0
while k:
    print(k)
 
    print('-----', k)







# n = 2, k = 2











