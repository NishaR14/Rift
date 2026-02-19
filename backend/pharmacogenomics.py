from typing import Dict, List, Optional

class PharmacogenomicAnalyzer:
    """Analyzes pharmacogenomic variants and determines phenotypes"""
    
    # Gene-specific variant databases (simplified - production would use CPIC/PharmGKB)
    GENE_VARIANTS = {
        'CYP2D6': {
            'rs1065852': {'star': '*10', 'effect': 'decreased'},
            'rs28371706': {'star': '*4', 'effect': 'null'},
            'rs3892097': {'star': '*4', 'effect': 'null'},
            'rs35742686': {'star': '*2', 'effect': 'normal'},
        },
        'CYP2C19': {
            'rs4244285': {'star': '*2', 'effect': 'null'},
            'rs4986893': {'star': '*3', 'effect': 'null'},
            'rs12248560': {'star': '*17', 'effect': 'increased'},
        },
        'CYP2C9': {
            'rs1799853': {'star': '*2', 'effect': 'decreased'},
            'rs1057910': {'star': '*3', 'effect': 'decreased'},
        },
        'SLCO1B1': {
            'rs4149056': {'star': '*5', 'effect': 'decreased'},
            'rs2306283': {'star': '*1b', 'effect': 'normal'},
        },
        'TPMT': {
            'rs1800462': {'star': '*2', 'effect': 'null'},
            'rs1142345': {'star': '*3A', 'effect': 'null'},
        },
        'DPYD': {
            'rs3918290': {'star': '*2A', 'effect': 'null'},
            'rs55886062': {'star': '*13', 'effect': 'null'},
            'rs67376798': {'star': '*9A', 'effect': 'decreased'},
        }
    }
    
    # Drug-gene associations
    DRUG_GENES = {
        'CODEINE': ['CYP2D6'],
        'WARFARIN': ['CYP2C9', 'VKORC1'],
        'CLOPIDOGREL': ['CYP2C19'],
        'SIMVASTATIN': ['SLCO1B1'],
        'AZATHIOPRINE': ['TPMT'],
        'FLUOROURACIL': ['DPYD'],
    }
    
    def analyze_variants(self, variants: List[Dict], drug_name: str) -> Dict:
        """
        Analyze variants for a specific drug and determine phenotype
        
        Returns pharmacogenomic profile with diplotype and phenotype
        """
        # Get relevant genes for drug
        relevant_genes = self.DRUG_GENES.get(drug_name.upper(), [])
        if not relevant_genes:
            return self._default_profile(drug_name)
        
        primary_gene = relevant_genes[0]
        
        # Find variants in relevant genes
        detected_variants = []
        gene_variants = {}
        
        for variant in variants:
            gene = variant.get('gene', '').upper()
            rsid = variant.get('rsid', '')
            
            if gene in [g.upper() for g in relevant_genes] or self._is_relevant_variant(rsid, relevant_genes):
                detected_variants.append({
                    'rsid': rsid or variant.get('rsid', 'unknown'),
                    'gene': gene or self._get_gene_from_rsid(rsid),
                    'chromosome': variant.get('chromosome'),
                    'position': variant.get('position'),
                    'reference': variant.get('reference'),
                    'alternate': variant.get('alternate'),
                    'star_allele': variant.get('star_allele') or variant.get('info', {}).get('STAR'),
                    'genotype': variant.get('genotype'),
                    'clinical_significance': self._get_clinical_significance(rsid, gene)
                })
                
                if gene:
                    gene_variants.setdefault(gene, []).append(variant)
        
        # Determine diplotype and phenotype
        diplotype, phenotype = self._determine_phenotype(primary_gene, gene_variants.get(primary_gene.upper(), []))
        
        return {
            'primary_gene': primary_gene,
            'diplotype': diplotype,
            'phenotype': phenotype,
            'detected_variants': detected_variants,
            'coverage_quality': 'good' if detected_variants else 'limited'
        }
    
    def _is_relevant_variant(self, rsid: str, genes: List[str]) -> bool:
        """Check if rsid is relevant for given genes"""
        for gene in genes:
            if gene.upper() in self.GENE_VARIANTS:
                if rsid in self.GENE_VARIANTS[gene.upper()]:
                    return True
        return False
    
    def _get_gene_from_rsid(self, rsid: str) -> Optional[str]:
        """Determine gene from rsid"""
        for gene, variants in self.GENE_VARIANTS.items():
            if rsid in variants:
                return gene
        return None
    
    def _get_clinical_significance(self, rsid: str, gene: str) -> str:
        """Get clinical significance of variant"""
        if gene.upper() in self.GENE_VARIANTS:
            if rsid in self.GENE_VARIANTS[gene.upper()]:
                effect = self.GENE_VARIANTS[gene.upper()][rsid]['effect']
                if effect == 'null':
                    return 'Loss of function'
                elif effect == 'decreased':
                    return 'Reduced function'
                elif effect == 'increased':
                    return 'Increased function'
        return 'Unknown'
    
    def _determine_phenotype(self, gene: str, variants: List[Dict]) -> tuple:
        """
        Determine diplotype and phenotype from variants
        
        Returns: (diplotype, phenotype)
        Phenotypes: PM (Poor Metabolizer), IM (Intermediate Metabolizer), 
                   NM (Normal Metabolizer), RM (Rapid Metabolizer), 
                   URM (Ultrarapid Metabolizer), Unknown
        """
        if not variants:
            return ('*1/*1', 'Unknown')
        
        # Extract star alleles from variants
        star_alleles = []
        for variant in variants:
            star = variant.get('star_allele') or variant.get('info', {}).get('STAR')
            if star:
                star_alleles.append(star)
            else:
                # Try to infer from rsid
                rsid = variant.get('rsid')
                if rsid and gene.upper() in self.GENE_VARIANTS:
                    if rsid in self.GENE_VARIANTS[gene.upper()]:
                        star_alleles.append(self.GENE_VARIANTS[gene.upper()][rsid]['star'])
        
        # If no star alleles found, try to infer from genotype
        if not star_alleles:
            genotype = variants[0].get('genotype')
            if genotype:
                # Simplified inference (production would use comprehensive diplotype tables)
                if '0/0' in genotype or '0|0' in genotype:
                    star_alleles = ['*1', '*1']
                elif '0/1' in genotype or '0|1' in genotype or '1/0' in genotype or '1|0' in genotype:
                    star_alleles = ['*1', '*2']
                elif '1/1' in genotype or '1|1' in genotype:
                    star_alleles = ['*2', '*2']
        
        # Default to *1/*1 if still no alleles
        if not star_alleles:
            star_alleles = ['*1', '*1']
        
        # Ensure we have two alleles
        if len(star_alleles) == 1:
            star_alleles.append('*1')
        elif len(star_alleles) > 2:
            star_alleles = star_alleles[:2]
        
        diplotype = f"{star_alleles[0]}/{star_alleles[1]}"
        
        # Determine phenotype based on star alleles
        phenotype = self._phenotype_from_diplotype(gene, star_alleles)
        
        return (diplotype, phenotype)
    
    def _phenotype_from_diplotype(self, gene: str, star_alleles: List[str]) -> str:
        """Determine phenotype from star allele diplotype"""
        # Simplified phenotype determination
        # Production would use CPIC/PharmGKB activity score tables
        
        null_alleles = {
            'CYP2D6': ['*4', '*5'],
            'CYP2C19': ['*2', '*3'],
            'CYP2C9': ['*2', '*3'],
            'TPMT': ['*2', '*3A', '*3B', '*3C'],
            'DPYD': ['*2A', '*13'],
        }
        
        increased_alleles = {
            'CYP2D6': ['*1xN', '*2xN'],
            'CYP2C19': ['*17'],
        }
        
        gene_upper = gene.upper()
        
        # Check for null alleles
        null_count = sum(1 for allele in star_alleles 
                        if gene_upper in null_alleles and 
                        any(null in allele for null in null_alleles[gene_upper]))
        
        # Check for increased function alleles
        increased_count = sum(1 for allele in star_alleles 
                            if gene_upper in increased_alleles and 
                            any(inc in allele for inc in increased_alleles[gene_upper]))
        
        if null_count == 2:
            return 'PM'  # Poor Metabolizer
        elif null_count == 1:
            return 'IM'  # Intermediate Metabolizer
        elif increased_count >= 1:
            if increased_count == 2 or 'xN' in ''.join(star_alleles):
                return 'URM'  # Ultrarapid Metabolizer
            else:
                return 'RM'  # Rapid Metabolizer
        else:
            return 'NM'  # Normal Metabolizer
    
    def _default_profile(self, drug_name: str) -> Dict:
        """Return default profile when no variants found"""
        return {
            'primary_gene': 'Unknown',
            'diplotype': '*1/*1',
            'phenotype': 'Unknown',
            'detected_variants': [],
            'coverage_quality': 'limited'
        }
