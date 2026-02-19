import re
from typing import Dict, List, Optional

class VCFParser:
    """Parser for VCF (Variant Call Format) files"""
    
    TARGET_GENES = ['CYP2D6', 'CYP2C19', 'CYP2C9', 'SLCO1B1', 'TPMT', 'DPYD']
    
    def parse_vcf(self, filepath: str) -> Dict:
        """
        Parse VCF file and extract pharmacogenomic variants
        
        Returns:
            Dict with 'success', 'variants', 'patient_id', and optional 'error'
        """
        try:
            variants = []
            patient_id = None
            header_info = {}
            
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    
                    # Skip empty lines
                    if not line:
                        continue
                    
                    # Parse header lines
                    if line.startswith('##'):
                        self._parse_header_line(line, header_info)
                        continue
                    
                    # Parse column header
                    if line.startswith('#CHROM'):
                        parts = line[1:].split('\t')
                        if len(parts) > 9:
                            patient_id = parts[9] if len(parts) > 9 else None
                        continue
                    
                    # Parse variant lines
                    if not line.startswith('#'):
                        variant = self._parse_variant_line(line, header_info)
                        if variant:
                            variants.append(variant)
            
            # Filter for pharmacogenomic variants
            pgx_variants = self._filter_pgx_variants(variants)
            
            return {
                'success': True,
                'variants': pgx_variants,
                'patient_id': patient_id or f'PATIENT_{hash(filepath) % 10000}',
                'total_variants': len(variants),
                'pgx_variants': len(pgx_variants)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'variants': []
            }
    
    def _parse_header_line(self, line: str, header_info: Dict):
        """Parse VCF header lines (##INFO, ##FORMAT, etc.)"""
        if line.startswith('##INFO='):
            # Extract INFO field definitions
            match = re.search(r'ID=([^,]+)', line)
            if match:
                info_id = match.group(1)
                header_info.setdefault('INFO', {})[info_id] = line
    
    def _parse_variant_line(self, line: str, header_info: Dict) -> Optional[Dict]:
        """Parse a single variant line from VCF"""
        parts = line.split('\t')
        
        if len(parts) < 8:
            return None
        
        chrom = parts[0]
        pos = parts[1]
        var_id = parts[2] if parts[2] != '.' else None
        ref = parts[3]
        alt = parts[4]
        qual = parts[5]
        filt = parts[6]
        info = parts[7]
        
        # Parse INFO field
        info_dict = self._parse_info_field(info)
        
        # Extract sample genotype if present
        genotype = None
        if len(parts) > 9:
            format_field = parts[8] if len(parts) > 8 else 'GT'
            sample_data = parts[9] if len(parts) > 9 else None
            if sample_data:
                genotype = self._parse_genotype(format_field, sample_data)
        
        variant = {
            'chromosome': chrom,
            'position': int(pos) if pos.isdigit() else None,
            'rsid': var_id or info_dict.get('RS', None),
            'reference': ref,
            'alternate': alt,
            'quality': qual,
            'filter': filt,
            'info': info_dict,
            'gene': info_dict.get('GENE', None),
            'star_allele': info_dict.get('STAR', None),
            'genotype': genotype
        }
        
        return variant
    
    def _parse_info_field(self, info_str: str) -> Dict:
        """Parse INFO field into dictionary"""
        info_dict = {}
        
        for item in info_str.split(';'):
            if '=' in item:
                key, value = item.split('=', 1)
                info_dict[key] = value
            else:
                info_dict[item] = True
        
        # Handle GENE, STAR, RS tags
        if 'GENE' in info_dict:
            info_dict['GENE'] = info_dict['GENE']
        if 'STAR' in info_dict:
            info_dict['STAR'] = info_dict['STAR']
        if 'RS' in info_dict:
            info_dict['RS'] = info_dict['RS']
        
        return info_dict
    
    def _parse_genotype(self, format_field: str, sample_data: str) -> Optional[str]:
        """Parse genotype from FORMAT and sample data"""
        format_keys = format_field.split(':')
        sample_values = sample_data.split(':')
        
        if 'GT' in format_keys:
            gt_idx = format_keys.index('GT')
            if gt_idx < len(sample_values):
                return sample_values[gt_idx]
        
        return None
    
    def _filter_pgx_variants(self, variants: List[Dict]) -> List[Dict]:
        """Filter variants to only include pharmacogenomic variants"""
        pgx_variants = []
        
        for variant in variants:
            gene = variant.get('gene')
            rsid = variant.get('rsid', '')
            
            # Check if variant is in target genes
            if gene and gene.upper() in [g.upper() for g in self.TARGET_GENES]:
                pgx_variants.append(variant)
            # Also check by rsid for known PGx variants
            elif rsid and self._is_pgx_rsid(rsid):
                pgx_variants.append(variant)
        
        return pgx_variants
    
    def _is_pgx_rsid(self, rsid: str) -> bool:
        """Check if rsid is a known pharmacogenomic variant"""
        # Common PGx rsids (simplified - in production, use comprehensive database)
        pgx_rsids = [
            'rs1065852', 'rs28371706', 'rs3892097',  # CYP2D6
            'rs4244285', 'rs4986893', 'rs12248560',  # CYP2C19
            'rs1799853', 'rs1057910',  # CYP2C9
            'rs4149056', 'rs2306283',  # SLCO1B1
            'rs1800462', 'rs1142345',  # TPMT
            'rs3918290', 'rs55886062', 'rs67376798'  # DPYD
        ]
        
        return rsid.upper() in [r.upper() for r in pgx_rsids]
