# MSSQL

---

## 1. 資料庫概念

- **資料庫（Database）**：用來系統化存放、管理資料的系統。  
- **關聯式資料庫（RDBMS）**：以表格形式存放資料，支援 SQL 語言操作。  
- **表格（Table）**：資料庫內的資料集合，每列是一筆資料，每欄是一個欄位。  
- **SQL（Structured Query Language）**：與資料庫溝通的標準語言。

---

## 2. 安裝 MSSQL（Docker 方式）

### 2.1 安裝 Docker
- 下載 [Docker Desktop](https://www.docker.com/products/docker-desktop/)  
- 安裝完成後，打開終端機確認：
```bash
docker -v
```
## 2.2 拉取 MSSQL 映像檔

使用官方映像檔，拉取最新 SQL Server 2019：

```bash
docker pull mcr.microsoft.com/mssql/server:2019-latest
```
說明：

這個指令會將 MSSQL 映像檔下載到本機。

後續啟動容器時會使用這個映像檔。

官方映像檔保證穩定性與安全性，建議使用最新版。

## 2.3 啟動 MSSQL 容器

使用剛下載的 MSSQL 映像檔啟動容器：

```bash
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=YourStrong!Passw0rd" \
   -p 1433:1433 --name mssql \
   -d mcr.microsoft.com/mssql/server:2019-latest
```
說明：

ACCEPT_EULA=Y：同意使用條款

SA_PASSWORD：設定管理員密碼，至少 8 碼，包含大小寫、數字與特殊符號

-p 1433:1433：將容器 SQL Server 的預設端口映射到本機，方便後端連線

--name mssql：給容器命名，方便管理

-d：在背景執行容器

檢查容器是否啟動：
```bash
docker ps
```
## 2.4 連線 MSSQL

### 使用 SQL Server Management Studio (SSMS)
- Server name：`localhost,1433`
- Authentication：SQL Server Authentication
- Login：`sa`
- Password：`YourStrong!Passw0rd`

### 使用命令列 sqlcmd
```bash
docker exec -it mssql /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "YourStrong!Passw0rd"
```
說明：

docker exec -it mssql ...：進入容器內部執行 sqlcmd

-S localhost：指定 SQL Server 服務位置

-U sa -P "YourStrong!Passw0rd"：使用管理員帳號登入