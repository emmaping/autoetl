# autoetl
xperf_to_collapsedstacks.py 这个文件不是我写的哈，放在一起是功能相近做个备份

自动对比两份Etl文件在DiskIO和CPU使用率的差别，从而定位性能下降的原因

Pre-condition
- Install Xperf
- Install python 2.7
- Get script from //depot/Symantec_Client_Security/Docs/qa/Performance/Performance Data/Tools/AutoETL/
- (Optional for CPU analysis) set _NT_SYMBOL_PATH = srv*%SystemDrive%\symbols*http://msdl.microsoft.com/download/symbols;C:\Mysymbols; _NT_SYMCACHE_PATH = %SystemDrive%\SymCache
- (Optional for CPU analysis) Unzip symbols.zip which delivered with Build to C:\Mysymbols

Usage
- Python AutoEtl.py –c <counter> –o <output> <etl1> <etl2>
- Support 2 counters :
  - cpu
  - diskio
