Text                                                                                                                                                                                                                                                           
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                                                                                                                                                                                                                                                             

                                                                                                                                                                                                                                                             

                                                                                                                                                                                                                                                             
--------------------------procedures
                                                                                                                                                                                                                         

                                                                                                                                                                                                                                                             
CREATE PROCEDure [sec].[mobile_bearer_token_get]
                                                                                                                                                                                                             
@status_code int = 0 OUTPUT
                                                                                                                                                                                                                                  
,@status_message varchar(200)='' output
                                                                                                                                                                                                                      
as
                                                                                                                                                                                                                                                           
BEGIN
                                                                                                                                                                                                                                                        
		DECLARE @token VARCHAR(32) = '';
                                                                                                                                                                                                                           
		DECLARE @char_set VARCHAR(75) = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
                                                                                                                                                          
		DECLARE @Length INT = 32;
                                                                                                                                                                                                                                  
		DECLARE @token_id VARCHAR(32) = '';
                                                                                                                                                                                                                        
		DECLARE @i INT = 1;
                                                                                                                                                                                                                                        

                                                                                                                                                                                                                                                             
	WHILE @i <= @Length
                                                                                                                                                                                                                                         
		BEGIN
                                                                                                                                                                                                                                                      
			SET @token_id = @token_id + SUBSTRING(@char_set, ABS(CHECKSUM(NEWID())) % LEN(@char_set) + 1, 1);
                                                                                                                                                         
			SET @i = @i + 1;
                                                                                                                                                                                                                                          
		END
                                                                                                                                                                                                                                                        

                                                                                                                                                                                                                                                             
		Set @token_id = @token_id;
                                                                                                                                                                                                                                 
		delete from secExpense. [sec].[mobile_token_master] where expire_datetime < GETDATE();
                                                                                                                                                                     
 
                                                                                                                                                                                                                                                            
		  insert into secExpense. [sec].[mobile_token_master] (token_id) values (@token_id);
                                                                                                                                                                       
		  if @@ROWCOUNT > 0
                                                                                                                                                                                                                                        
			  BEGIN		
                                                                                                                                                                                                                                                 
				  Select @status_code = 200;
                                                                                                                                                                                                                             
				  Select @status_message = 'Created';	  
                                                                                                                                                                                                                 
			  END
                                                                                                                                                                                                                                                     
	ELSE
                                                                                                                                                                                                                                                        
	  BEGIN
                                                                                                                                                                                                                                                     
	  Select '' token_id;
                                                                                                                                                                                                                                       
		  Select @status_code = 400;
                                                                                                                                                                                                                               
		  Select @status_message = 'Token Generation Failed';
                                                                                                                                                                                                      
	  END
                                                                                                                                                                                                                                                       

                                                                                                                                                                                                                                                             
	 Select @token_id token_id, @status_code status_code, @status_message status_message;
                                                                                                                                                                       
END
                                                                                                                                                                                                                                                          
