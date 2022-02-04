Architecture:

Key point : 
- create one time use url for per request
    OBSERVATION:
     form this statement i can say that  we are not going to one (actual_url --> hash_url) mapping.
     suppose we have two user  deepak , akshay. both uses our url shortner tool and received hasted_url https:www.host_name.com/f6h for https:www.youtube.com . if deepak uses our shorten url then akshay will not able to use same due to one time use policy.
     So , in order to fulfill our one time use policy we must have different hashed_url for https:www.youtube.com per request to avoid collision.

- avoid losing url from formatter
    OBSERVATION:
    almost all formatter target non-alphanumeric value for formatting.In order to avoid this issue with generate hashed_url with only alphanumeric values.


APPROCH 1:
    -https://HOST_NAME/<short_hash_string>
     
    step1-basic idea is to generate random short_hash_string string of length (6)
    step2-check if this short_hash_string is not present in DB then insert short_hash_string into DB with actual_url mapping
    step2-if this  short_hash_string is present , repeat step 1 
    
    Limitation on this approch:
        for every new request we have look over DB to check wether currently generated string is present in DB or not.

APPROCH 2 (applied on this project):
    - https://HOST_NAME/<short_hash_string>

    In my case length of short_hash_string is >=1 and <=6
    
    There are 62 alphanumeric charactor and x is one of alphanumeric charactor
    short_hash_string  combinations
    x                  = 64   
    xx                 = 64*64 = 4096 
    xxx                = 64*64*64 = 262144 
    xxxx               = 64*64*64*64 = 16777216 
    xxxxx              = 64*64*64*64*64 = 1073741824  
    xxxxxx             = 64*64*64*64*64*64 = 68719476736  

    We provide url upto 69809999936 (sum of above combination) if just insert short_hash_string-->actual_url mapping without looking for short_hash_string in DB.

    Now our problem shorten to 'generate a unqiue hash for a interger' and 'from this generated unique_hash i can revert back to integer'. So we can use the concept of base conversion
    
    Functions description:
    getIdFromHash : 
    params: get 1 param "string" consist of alphanumeric chars with size from 1 to 6
    return a integer value

    getHashValueFromId : 
    params: get one param "int" can be any ineger between 1-69809999936 
    return: return a hashed  value 

SYSTEM FLOW:
    WHEN CLIENT WANT TO GET SHORTEN URL:
        * client send a url_short request to server
        * server first get the last row from data in order to extarct id from it.
            if there is no row then 
                id = 1
            else:
                id =last_id +1

        * then it call  getHashValueFromId() and it will generate a hashed url 
        * save it to datebase ( id , actual_url , hashed_url)
    
    WHEN CLIENT WANT TO CLICK ON SHORTEN URL:
        * Client clicked on hashed_url.
        * Server call getIdFromHash() and retrive id corresponding to the hashed_url.
        * Then server hit database in-order to find the row with primary_key = id.
            if there is no row in DB
                then we return the BAD_REQUEST ERROR. In that case either shorten_url already used or no row in inserted for the requested id.
            else 
                we receive the matched row.
        * Now we have matched row , retrive actual url
        * Delete entry for this id from database 
        * Redirect the user to actual url.










