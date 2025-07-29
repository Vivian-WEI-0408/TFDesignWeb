import dnacauldron
class SupportGG:
    def __init__(self,PartAddress_list, PartName_list):
        self.PartAddress_List = PartAddress_list
        self.PartName_List = PartName_list
        self.repository = dnacauldron.SequenceRepository()

    def assemblyPart(self,name):
        temp = len(self.repository.get_all_part_names())
        if(len(self.repository.get_all_part_names())!=0):
            self.repository = dnacauldron.SequenceRepository()
        self.repository.import_records(files=self.PartAddress_List,use_file_names_as_ids=False, topology='default_to_circular')
        assembly = dnacauldron.Type2sRestrictionAssembly(parts=self.PartName_List, name = name)
        # assembly = dnacauldron.Type2sRestrictionAssembly(parts=self.PartName_List,expect_no_unused_parts=False)
        self.simulation = assembly.simulate(sequence_repository=self.repository)
        # assert len(self.simulation.construct_records) == 1
        # assert len(self.simulation.construct_records[0]) == 8016


    def show(self):
        report_writer = dnacauldron.AssemblyReportWriter(include_mix_graphs=True, include_assembly_plots=True)
        self.simulation.write_report("output", report_writer=report_writer)


    def AddPart(self, records):
        self.repository.add_records(records)