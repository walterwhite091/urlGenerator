## Architecture:

##### Key points  
- Create one time use url for per request
     - Form this statement i can say that  we are not going to one (actual_url --> hash_url)    mapping.
     - Suppose we have two user  deepak , akshay. both uses our URL shortner tool and received hasted_url **https:www.<host_name>.com/f6h**  for  **https:www.youtube.com** . If deepak uses our shorten URL then akshay will not able to use same shorten URL due to one time use policy.
     - So , In order to fulfill our one time use policy we must have different hashed_url for **https:www.youtube.com**  per request to avoid collision.

- Avoid losing url from formatter
    - Almost all formatter target non-alphanumeric value for formatting. In order to avoid this issue with generate hashed_url with only alphanumeric values.

---
#### APPROCH 1
>https://HOST_NAME/<short_hash_string>
     
1. Basic idea is to generate random short_hash_string string of length (6)
2. Check if 
    - this short_hash_string is not present in DB then insert short_hash_string into DB with actual_url mapping
    - If this  short_hash_string is present , repeat step 1 
    
##### Limitation on this approch
>for every new request we have look over DB to check wether currently generated string is present in DB or not which is not efficent if try to scale it.

---
#### APPROCH 2 (Applied on this project):
>https://HOST_NAME/<short_hash_string>

*For this  project length of short_hash_string is >=1 and <=6*
| ID | actual_url | short_hash_string
| ----------- | ----------- | ----------- |
| 1 | https://www.youtube.com/ | hash1
| 2 | https://www.youtube.com/ | hash2
| n | nth_URL | nth_hash | 

    
    There are 62 alphanumeric charactor and x is one of alphanumeric charactor
    short_hash_string  combinations
    x                  = 62   
    xx                 = 62*62 = 3844 
    xxx                = 62*62*62 = 246016 
    xxxx               = 62*62*62*62 = 15252992 
    xxxxx              = 62*62*62*62*62 = 945685504  
    xxxxxx             = 62*62*62*62*62*62 = 58632501248  

    -We can provide diffrent url upto 69809999936 (sum of above combination) if we just insert (short_hash_string --> actual_url) mapping without looking for short_hash_string in DB and just increment the primary key ID.
    
    - Now our problem shorten to 'generate a unqiue hash for a interger' and 'from this generated unique_hash i can revert back to integer'.
---
#### Function Description
*We can use the concept of base conversion* . [click here](https://www.tutorialspoint.com/computer_logical_organization/number_system_conversion.htm) to learn more about base conversion.

Functions description:
- getIdFromHash : 
params: get 1 param "string" consist of alphanumeric chars with size from 1 to 6
return a integer value

- getHashValueFromId : 
params: get one param "int" can be any ineger between 1-69809999936 
return: return a hashed  value 


---
#### SYSTEM FLOW:
- WHEN CLIENT WANT TO GET SHORTEN URL
    1. client send a url_short request to server
    2. server first get the last row from data in order to extarct id from it.
        - if there is no row then **ID = 1**
        - else **ID =last_id +1**

    3. Then it call  getHashValueFromId() and it will generate a hashed url 
    4. Save it to datebase ( ID , actual_url , short_hash_string)
    
- WHEN CLIENT WANT TO CLICK ON SHORTEN URL
    1. Client clicked on hashed_url.
    2. Server call getIdFromHash() and retrive id corresponding to the hashed_url.
    3. Then server hit database in-order to find the row with primary_key = id.
        - if there is no row in DB
                - Then we return the **BAD_REQUEST ERROR** or Redirect user to **invalid-url** page In that case either shorten_url already used or no row in inserted for the requested id.
        - else 
            - we receive the matched row.
    4. Now we have matched row , retrive actual url
    5. Delete entry for this id from database 
    6. Redirect the user to actual url.
    












