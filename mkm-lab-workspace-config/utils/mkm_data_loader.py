#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MKM-12 통합 이론 데이터 로더
구조화된 JSON 데이터를 쉽게 로드하고 사용할 수 있는 유틸리티
"""

import json
from pathlib import Path
from typing import Dict, List, Optional


class MKMDataLoader:
    """MKM-12 데이터 로더 클래스"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Args:
            data_dir: JSON 데이터 파일들이 있는 디렉토리 경로
        """
        self.data_dir = Path(data_dir)
        self._personas = None
        self._forces = None
        self._modes = None
        self._glossary = None
        self._imbalance_patterns = None
        self._naming_conventions = None
    
    def load_personas(self) -> Dict:
        """12 페르소나 데이터 로드"""
        if self._personas is None:
            file_path = self.data_dir / "personas.json"
            with open(file_path, 'r', encoding='utf-8') as f:
                self._personas = json.load(f)
        return self._personas
    
    def load_forces(self) -> Dict:
        """4 Forces 데이터 로드"""
        if self._forces is None:
            file_path = self.data_dir / "forces.json"
            with open(file_path, 'r', encoding='utf-8') as f:
                self._forces = json.load(f)
        return self._forces
    
    def load_modes(self) -> Dict:
        """3 Manifestation Modes 데이터 로드"""
        if self._modes is None:
            file_path = self.data_dir / "manifestation_modes.json"
            with open(file_path, 'r', encoding='utf-8') as f:
                self._modes = json.load(f)
        return self._modes
    
    def load_glossary(self) -> Dict:
        """용어사전 데이터 로드"""
        if self._glossary is None:
            file_path = self.data_dir / "glossary.json"
            with open(file_path, 'r', encoding='utf-8') as f:
                self._glossary = json.load(f)
        return self._glossary
    
    def load_imbalance_patterns(self) -> Dict:
        """불균형 패턴 데이터 로드"""
        if self._imbalance_patterns is None:
            file_path = self.data_dir / "imbalance_patterns.json"
            with open(file_path, 'r', encoding='utf-8') as f:
                self._imbalance_patterns = json.load(f)
        return self._imbalance_patterns
    
    def load_naming_conventions(self) -> Dict:
        """명명 규칙 데이터 로드"""
        if self._naming_conventions is None:
            file_path = self.data_dir / "naming_conventions.json"
            with open(file_path, 'r', encoding='utf-8') as f:
                self._naming_conventions = json.load(f)
        return self._naming_conventions
    
    def get_persona_by_code(self, code: str) -> Optional[Dict]:
        """코드로 페르소나 찾기"""
        personas = self.load_personas()
        for persona in personas['personas']:
            if persona['code'] == code:
                return persona
        return None
    
    def get_personas_by_force(self, force: str) -> List[Dict]:
        """특정 Force의 모든 페르소나 찾기"""
        personas = self.load_personas()
        return [p for p in personas['personas'] if p['force'] == force]
    
    def get_personas_by_mode(self, mode: str) -> List[Dict]:
        """특정 Mode의 모든 페르소나 찾기"""
        personas = self.load_personas()
        return [p for p in personas['personas'] if p['mode'] == mode]
    
    def get_force_by_code(self, code: str) -> Optional[Dict]:
        """코드로 Force 찾기"""
        forces = self.load_forces()
        for force in forces['forces']:
            if force['code'] == code:
                return force
        return None
    
    def get_mode_by_code(self, code: str) -> Optional[Dict]:
        """코드로 Mode 찾기"""
        modes = self.load_modes()
        for mode in modes['modes']:
            if mode['code'] == code:
                return mode
        return None
    
    def search_personas(self, keyword: str) -> List[Dict]:
        """키워드로 페르소나 검색"""
        personas = self.load_personas()
        results = []
        keyword_lower = keyword.lower()
        
        for persona in personas['personas']:
            # 한글명, 영문명, 핵심 기능에서 검색
            if (keyword_lower in persona['korean_name'].lower() or
                    keyword_lower in persona['english_name'].lower() or
                    keyword_lower in persona['core_function'].lower()):
                results.append(persona)
        
        return results
    
    def get_balancing_personas(self, persona_code: str) -> List[Dict]:
        """특정 페르소나의 조정 페르소나들 찾기"""
        persona = self.get_persona_by_code(persona_code)
        if not persona:
            return []
        
        balancing_codes = persona.get('balancing_personas', [])
        balancing_personas = []
        
        for code in balancing_codes:
            balancing_persona = self.get_persona_by_code(code)
            if balancing_persona:
                balancing_personas.append(balancing_persona)
        
        return balancing_personas
    
    def get_imbalance_patterns(self) -> List[Dict]:
        """모든 불균형 패턴 가져오기"""
        data = self.load_imbalance_patterns()
        return data.get('imbalance_patterns', [])
    
    def get_transition_patterns(self) -> Dict:
        """전이 패턴 정보 가져오기"""
        data = self.load_imbalance_patterns()
        return data.get('transition_concepts', {})
    
    def export_persona_summary(self, output_file: str = "persona_summary.txt"):
        """페르소나 요약을 텍스트 파일로 내보내기"""
        personas = self.load_personas()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("MKM-12 페르소나 요약\n")
            f.write("=" * 50 + "\n\n")
            
            for persona in personas['personas']:
                f.write(f"코드: {persona['code']}\n")
                f.write(f"한글명: {persona['korean_name']}\n")
                f.write(f"영문명: {persona['english_name']}\n")
                f.write(f"핵심 기능: {persona['core_function']}\n")
                f.write(f"조정 페르소나: {', '.join(persona['balancing_personas'])}\n")
                f.write("-" * 30 + "\n\n")
        
        print(f"페르소나 요약이 {output_file}에 저장되었습니다.")


def main():
    """사용 예시"""
    loader = MKMDataLoader()
    
    # S-B 페르소나 정보 가져오기
    s_b = loader.get_persona_by_code("S-B")
    if s_b:
        print(f"S-B 페르소나: {s_b['korean_name']}")
        print(f"핵심 기능: {s_b['core_function']}")
        print(f"조정 페르소나: {s_b['balancing_personas']}")
    
    # Solar Force의 모든 페르소나
    solar_personas = loader.get_personas_by_force("S")
    print(f"\nSolar Force 페르소나: "
          f"{[p['code'] for p in solar_personas]}")
    
    # 키워드 검색
    search_results = loader.search_personas("개시")
    print(f"\n'개시' 검색 결과: "
          f"{[p['code'] for p in search_results]}")
    
    # 페르소나 요약 내보내기
    loader.export_persona_summary()


if __name__ == "__main__":
    main() 