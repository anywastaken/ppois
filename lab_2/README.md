Classes
-------
AssembledDetail 7 0 -> Detail  
Assembly 7 0 -> Detail  
Blueprint 7 0 -> Material  
Detail 6 0 ->  
Disk 8 2 ->  
Instruction 6 0 ->  
ProducedDetail 6 0 ->  
Tire 9 2 ->  
Wheel 7 0 -> Disk Tire  
AssemblyMachine 6 3 -> Assembly AssembledDetail  
DiskMachine 6 3 -> Disk BluePrint  
Machine 6 3 -> BluePrint Assembly Detail  
ProductionMachine 6 3 -> BluePrint ProducedDetail  
TireMachine 6 3 -> Tire BluePrint  
WheelAssemblyMachine 6 3 -> Disk Tire Wheel Assembly
DefectReport 5 1 -> Detail Worker Machine Maintenance  
Factory 5 0 -> Workshop FactoryExport FactoryImport InnerStorage  
FactoryExport 2 3 -> DeliveryTruck Warehouse  
FactoryImport 2 2 -> InnerStorage  
InnerStorage 3 2 -> Detail Material FactoryExport  
Maintenance 2 3 -> Machine DefectReport  
ProductionLine 4 8 -> Detail Machine Maintenance FactoryExport InnerStorage
Workshop 4 0 -> ProductionLine  
CastIron 5 2 ->  
Glass 4 2 ->  
Material 4 1 ->  
Rubber 5 2 ->  
StainlessSteel 5 2 ->  
Steel 5 2 ->  
Wood 5 2 ->  
SocialNetwork 3 2 ->  
Accountant 3 2 ->  
Driver 4 2 ->  
Employee 3 0 ->  
Engineer 4 3 -> Machine Maintenance  
GeneralManager 4 1 -> Contract  
Lawyer 4 2 -> GeneralManager Condition Contract Supplier  
Manager 4 2 -> Worker  
Security 4 2 -> DeliveryTruck  
Smm 6 3 -> SocialNetwork  
Worker 8 5 -> DefectReport Detail Machine ProductionLine Employee  
Condition 3 0 ->  
Contract 7 0 -> GeneralManager Condition Supplier  
DeliveryTruk 5 3 -> Detail Driver Warehouse  
DetailStorageCell 3 3 -> Detail WarehouseExport  
MaterialStorageCell 3 3 -> Material WarehouseExport  
Supplier 3 1 -> Contract  
Warehouse 9 0 -> Security DeliveryTruck DetailStorageCell MaterialStorageCell WarehouseExport WarehouseImport
WarehouseExport 3 6 -> DeliveryTruck
WarehouseImport 3 5 -> Detail Material

Exceptions (12)
---------------
ExportDirectionError, ImportDirectionError, InsufficientDetailsError, InsufficientMaterialsError, MachineAlreadyRunningError, MachineNotRunningError, MissingAttributeError, NoImportModuleError, NotEnoughItemsForTruckError, StorageOverflowError, TruckSizeError, WrongDefectChanceValue

Summary
-------
Classes: 50  
Fields: 245  
Behaviors: 100  
Associations: 77  
Exceptions: 12