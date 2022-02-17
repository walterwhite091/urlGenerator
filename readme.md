## Architecture:

##### Key points  
- No length restriction
     - There should be no limit on URL length. For that puspose not using inbuild URL_FIELD feature , because most of them provide support upto 200 char limit and some upto 1000. so we will receive free text from user and validate url on server end.
  
- Avoid losing url from formatter
    - Almost all formatter target non-alphanumeric value for formatting. In order to avoid this issue we will generate hashed_url with only alphanumeric values.
- Link Tracker
    - *We will also manage no of times user clicked the valid short url .*
     
---
#### APPROCH 1
>https://HOST_NAME/<short_hash_string>
     
1. Basic idea is to generate random short_hash_string string of length (6)
2. Check if 
    - this short_hash_string is not present in DB then insert short_hash_string into DB with actual_url mapping with hit_count=0.
    - If this  short_hash_string is present , repeat step 1 
 
    
##### Limitation on this approch
>for every new request we have look over DB to check wether currently generated string is present in DB or not which is not efficent if try to scale it.

---
#### APPROCH 2 (Applied on this project):
>https://HOST_NAME/<short_hash_string>

*For this  project length of short_hash_string is >=1 and <=6*

>*This is the respresentation of our schema*

| ID | actual_url | short_hash_string | hit_count
| ----------- | ----------- | ----------- | -----------
| 1 | https://www.youtube.com/ | hash1  | 0
| 2 | https://www.youtube.com/ | hash2  | 2
| n | nth_URL | nth_hash | 102

    
    There are 62 alphanumeric charactor and x is one of alphanumeric charactor
    short_hash_string  combinations
    x                  = 62   
    xx                 = 62*62 = 3844 
    xxx                = 62*62*62 = 246016 
    xxxx               = 62*62*62*62 = 15252992 
    xxxxx              = 62*62*62*62*62 = 945685504  
    xxxxxx             = 62*62*62*62*62*62 = 58632501248  

    -We can provide diffrent url upto 58632501248 (sum of above combination) if we just insert (short_hash_string --> actual_url) mapping without looking for short_hash_string in DB and just increment the primary key ID.
    
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
               - increase hit_count by 1
    4. Now we have matched row , retrive actual url
    5. Delete entry for this id from database 
    6. Redirect the user to actual url.
    












