library(httr)
library(jsonlite)

### Input to the code ####
## Right click on the zerodha chart page and go to inspect element, go to network, find the chart link and extract below values

symbol_list<-read.csv("E:/Repo/AlgoModels/IntradayDatasetPrep/top10.csv")
path_to_store_data<-"E:/Repo/AlgoModels/IntradayDatasetPrep/5mins_data/"

cfduid="d4d0d328159520c485d608749969c5a131618825755"
enctoken="enctoken JFnx4wVvksY146GQkGpuGOX/of2WvL06t3ZhDQoZkaaQgV4ZM3SMSkEVEN9iV2s249sHIQPuCyex93M7QyDA4FypAnHyTg=="
kf_session="byjSztZA0tVClV9p4DTfwMNdCpj44GB1"
public_token="0ezIZjCGwdnZxPS6qrHgREiliESqt0uP"

user_id="MG3933"

from="2016-01-01"
to="2021-04-24"

st <- as.Date(from)
en <- as.Date(to)

### Specify Interval
## minute,2minute,3minute,4minute,10minute,15minute,60minute,day

interval="5minute"

i=1
for (i in 1:nrow(symbol_list)){
  ID=symbol_list[i,2]
  symbol_name=symbol_list[i,1]
  print(ID)
  print(symbol_name)
  
  theDate <-st
  datalist = list()
  big_data<-data.frame()
  while (theDate<=en)
    
  {
    
    NextDate<-  as.Date(theDate+30)
    
    if (NextDate > as.Date(Sys.Date())){
      NextDate<-en
    }  
    dt_range=paste0(theDate,"&to=",NextDate)
    print(dt_range)  
    
    url<- paste0("https://kite.zerodha.com/oms/instruments/historical/",ID,"/",interval)
    httr::GET(
      url = url,
      add_headers(authorization=enctoken),
      query = list(
        user_id = user_id,
        oi = "1",
        from = theDate,
        to = NextDate,
        kf_session= kf_session,
        public_token=public_token,
        user_id= user_id,
        enctoken= enctoken
      )
    ) -> res
    
    dat <- httr::content(res)
    
    jsonRespText<-content(res,as="text")
    print(jsonRespText)
    document<-fromJSON(txt=jsonRespText)
    
    x<-document[["data"]]
    y<-x[["candles"]]
    
    
    
    if (length(y) <5){
      next
      print("hi")
      
      print(theDate)
      
    }
    
    
    dt<-as.data.frame(document)
    dt<-dt[-1]
    colnames(dt)[1]<-"TIME"
    colnames(dt)[2]<-"Open"
    colnames(dt)[3]<-"High"
    colnames(dt)[4]<-"Low"
    colnames(dt)[5]<-"Close"
    colnames(dt)[6]<-"Volume"
    colnames(dt)[7]<-"SYMBOL"
    dt$SYMBOL<-symbol_name
    
    dt$TIME<-gsub("\\+0530","",dt$TIME)
    
    dt$TIME<-gsub("T"," ",dt$TIME)
    dt$Date <- as.Date(dt$TIME) #already got this one from the answers above
    dt$TIME1 <- format(as.POSIXct(dt$TIME) ,format = "%H:%M:%S")
    datalist[[i]] <- dt
    print("4")
    
    theDate<-as.Date(theDate)+30
    
    big_data = rbind(big_data,dt)
  }
  
  
  file= paste0(path_to_store_data,symbol_name,".csv",sep="")
  write.csv(big_data,file,row.names = F)
  
  
  print(theDate)  
}





