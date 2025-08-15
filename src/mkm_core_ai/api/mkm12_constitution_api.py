"""
MKM-12 Constitutional AI API

FastAPI endpoints for constitutional analysis and ethical decision-making.
Provides REST API access to the Constitution Engine functionality.
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
import logging
import sys
import os
from datetime import datetime
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mkm12.types import (
    ConstitutionAnalysisInput, ConstitutionAnalysisResult, 
    SystemHealthStatus, BiometricData, PsychologicalProfile, 
    BehavioralData, ConstitutionType
)
from mkm12.constitution_engine import get_constitution_engine, ConstitutionEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="MKM-12 Constitutional AI API",
    description="Constitutional analysis and ethical decision-making API based on traditional Korean medicine",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get constitution engine
def get_engine() -> ConstitutionEngine:
    """Dependency to get constitution engine instance"""
    return get_constitution_engine()

@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup"""
    logger.info("🚀 Starting MKM-12 Constitutional AI API")
    engine = get_constitution_engine()
    health = engine.get_health_status()
    logger.info(f"✅ Constitution Engine initialized - Status: {health['status']}")

@app.on_event("shutdown") 
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Shutting down MKM-12 Constitutional AI API")

# Health and Status Endpoints

@app.get("/health", response_model=Dict[str, Any])
async def health_check(engine: ConstitutionEngine = Depends(get_engine)):
    """
    Health check endpoint for system monitoring
    
    Returns:
        System health status and statistics
    """
    try:
        health_status = engine.get_health_status()
        
        # Convert to SystemHealthStatus model for validation
        system_health = SystemHealthStatus(
            status=health_status["status"],
            version=health_status["version"],
            uptime_seconds=health_status["uptime_seconds"],
            total_analyses=health_status["total_analyses"],
            total_ethical_decisions=health_status["total_ethical_decisions"],
            error_rate=health_status["error_rate"]
        )
        
        return system_health.dict()
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/status")
async def api_status():
    """
    Simple API status endpoint
    
    Returns:
        Basic API status information
    """
    return {
        "api": "MKM-12 Constitutional AI",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "health": "/health",
            "constitution_analysis": "/analyze/constitution",
            "ethical_decisions": "/ethics/summary",
            "constitution_types": "/constitution/types"
        }
    }

# Constitution Analysis Endpoints

@app.post("/analyze/constitution", response_model=ConstitutionAnalysisResult)
async def analyze_constitution(
    analysis_input: ConstitutionAnalysisInput,
    background_tasks: BackgroundTasks,
    engine: ConstitutionEngine = Depends(get_engine)
):
    """
    Perform constitutional analysis based on user data
    
    Args:
        analysis_input: User data for constitutional analysis
        
    Returns:
        Constitutional analysis result with predicted type and recommendations
    """
    try:
        logger.info(f"🔬 Starting constitution analysis for user: {analysis_input.user_id}")
        
        # Perform the analysis
        result = engine.analyze_constitution(analysis_input)
        
        # Add background task for logging (optional)
        background_tasks.add_task(
            log_analysis_result, 
            analysis_input.user_id, 
            result.predicted_constitution.value,
            result.confidence_score
        )
        
        logger.info(f"✅ Analysis completed: {result.predicted_constitution.value} ({result.confidence_score:.2f})")
        return result
        
    except ValueError as e:
        logger.warning(f"⚠️ Invalid input for constitution analysis: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Constitution analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze/constitution/batch")
async def analyze_constitution_batch(
    analysis_inputs: List[ConstitutionAnalysisInput],
    engine: ConstitutionEngine = Depends(get_engine)
):
    """
    Perform batch constitutional analysis for multiple users
    
    Args:
        analysis_inputs: List of user data for constitutional analysis
        
    Returns:
        List of constitutional analysis results
    """
    if len(analysis_inputs) > 10:
        raise HTTPException(status_code=400, detail="Batch size limited to 10 analyses")
    
    results = []
    errors = []
    
    for i, analysis_input in enumerate(analysis_inputs):
        try:
            result = engine.analyze_constitution(analysis_input)
            results.append(result)
        except Exception as e:
            errors.append({
                "index": i,
                "user_id": analysis_input.user_id,
                "error": str(e)
            })
    
    return {
        "results": results,
        "errors": errors,
        "total_processed": len(analysis_inputs),
        "successful": len(results),
        "failed": len(errors)
    }

# Constitution Information Endpoints

@app.get("/constitution/types")
async def get_constitution_types():
    """
    Get information about all constitution types
    
    Returns:
        Complete list of constitution types with descriptions
    """
    try:
        engine = get_constitution_engine()
        constitution_data = engine.constitution_data
        
        types_info = {}
        for const_type in ConstitutionType:
            const_data = constitution_data.get("constitution_types", {}).get(const_type.value, {})
            types_info[const_type.value] = {
                "name": const_data.get("name", ""),
                "name_en": const_data.get("name_en", ""),
                "base_type": const_data.get("base_type", ""),
                "subtype": const_data.get("subtype", ""),
                "description": const_data.get("description", ""),
                "characteristics": const_data.get("characteristics", {})
            }
        
        return {
            "constitution_types": types_info,
            "total_types": len(ConstitutionType),
            "base_constitutions": constitution_data.get("base_constitutions", {})
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get constitution types: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve constitution types: {str(e)}")

@app.get("/constitution/{constitution_type}")
async def get_constitution_details(constitution_type: ConstitutionType):
    """
    Get detailed information about a specific constitution type
    
    Args:
        constitution_type: The constitution type to get details for
        
    Returns:
        Detailed constitution information including characteristics and recommendations
    """
    try:
        engine = get_constitution_engine()
        characteristics = engine._get_constitution_characteristics(constitution_type)
        constitution_data = engine.constitution_data.get("constitution_types", {}).get(constitution_type.value, {})
        
        return {
            "constitution_type": constitution_type.value,
            "characteristics": characteristics.dict(),
            "health_management": constitution_data.get("health_management", {}),
            "traditional_medicine": constitution_data.get("traditional_medicine", {}),
            "base_type": constitution_data.get("base_type", ""),
            "subtype": constitution_data.get("subtype", "")
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get constitution details: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve constitution details: {str(e)}")

# Ethics and Decisions Endpoints

@app.get("/ethics/summary")
async def get_ethical_summary(engine: ConstitutionEngine = Depends(get_engine)):
    """
    Get summary of ethical decisions made by the system
    
    Returns:
        Ethical decisions summary with statistics and recent decisions
    """
    try:
        summary = engine.get_ethical_summary()
        return summary
        
    except Exception as e:
        logger.error(f"❌ Failed to get ethical summary: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve ethical summary: {str(e)}")

@app.post("/ethics/evaluate")
async def evaluate_ethical_decision(
    action: str,
    context: Dict[str, Any],
    engine: ConstitutionEngine = Depends(get_engine)
):
    """
    Evaluate an action against ethical principles
    
    Args:
        action: The action to evaluate
        context: Context for the ethical decision
        
    Returns:
        Ethical decision result
    """
    try:
        from mkm12.types import EthicalDecisionContext, DataType
        
        # Convert context dict to EthicalDecisionContext
        ethical_context = EthicalDecisionContext(
            action_type=action,
            data_types=[DataType(dt) for dt in context.get("data_types", [])],
            patient_data_involved=context.get("patient_data_involved", False),
            anonymized=context.get("anonymized", False),
            explainable=context.get("explainable", False),
            medical_benefit_score=context.get("medical_benefit_score"),
            risk_level=context.get("risk_level"),
            additional_context=context.get("additional_context", {})
        )
        
        decision = engine._make_ethical_decision(action, ethical_context)
        
        return {
            "decision_id": decision.decision_id,
            "action": action,
            "decision": decision.decision.value,
            "principle": decision.principle.value,
            "confidence": decision.confidence,
            "reasoning": decision.reasoning,
            "requires_human_review": decision.requires_human_review,
            "timestamp": decision.timestamp.isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Ethical evaluation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Ethical evaluation failed: {str(e)}")

# Testing and Demo Endpoints

@app.post("/test/sample-analysis")
async def create_sample_analysis(engine: ConstitutionEngine = Depends(get_engine)):
    """
    Create a sample constitutional analysis for testing purposes
    
    Returns:
        Sample analysis result
    """
    try:
        # Create sample test data
        sample_input = ConstitutionAnalysisInput(
            user_id=f"demo_user_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            biometric_data=BiometricData(
                heart_rate=75.0,
                temperature=36.7,
                blood_pressure_systolic=120,
                blood_pressure_diastolic=80
            ),
            psychological_data=PsychologicalProfile(
                energy_level=6.5,
                stress_level=5.0,
                personality_traits={
                    "extraversion": 0.7,
                    "creativity": 0.6,
                    "stability": 0.8
                }
            ),
            behavioral_data=BehavioralData(
                activity_level="moderate",
                sleep_pattern={"duration": 7.5, "quality": "good"},
                dietary_preferences=["balanced", "traditional"],
                exercise_habits={"frequency": "regular", "intensity": "moderate"}
            )
        )
        
        result = engine.analyze_constitution(sample_input)
        
        return {
            "message": "Sample analysis completed",
            "result": result,
            "note": "This is a demo analysis with sample data"
        }
        
    except Exception as e:
        logger.error(f"❌ Sample analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Sample analysis failed: {str(e)}")

@app.get("/test/engine-test")
async def run_engine_test():
    """
    Run a comprehensive test of the constitution engine
    
    Returns:
        Test results and system status
    """
    try:
        # Import the test function
        from mkm12.constitution_engine import test_constitution_engine
        
        # Capture test output (simplified version)
        engine = test_constitution_engine()
        health = engine.get_health_status()
        ethical = engine.get_ethical_summary()
        
        return {
            "test_status": "completed",
            "engine_health": health,
            "ethical_summary": ethical,
            "message": "Constitution engine test completed successfully"
        }
        
    except Exception as e:
        logger.error(f"❌ Engine test failed: {e}")
        raise HTTPException(status_code=500, detail=f"Engine test failed: {str(e)}")

# Background task functions

async def log_analysis_result(user_id: str, constitution: str, confidence: float):
    """Background task to log analysis results"""
    logger.info(f"📊 Analysis logged - User: {user_id}, Constitution: {constitution}, Confidence: {confidence:.2f}")

# Error handlers

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"❌ Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": 500,
            "timestamp": datetime.now().isoformat()
        }
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "api": "MKM-12 Constitutional AI",
        "version": "1.0.0",
        "description": "Constitutional analysis and ethical decision-making API",
        "docs": "/docs",
        "health": "/health",
        "status": "/status"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)