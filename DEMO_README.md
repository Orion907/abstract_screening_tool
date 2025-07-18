# Abstract Screening Tool - Demo

🚀 **Automated systematic review screening using AI** 

This demo showcases an AI-powered tool for screening research abstracts based on PIC (Population, Intervention, Comparator) criteria.

## 🎯 Demo Features

### ✅ Core Functionality
- **PIC Criteria Input** - Template-based or custom criteria entry
- **CSV File Upload** - Drag-and-drop with validation
- **AI-Powered Screening** - OpenAI GPT models for decision making
- **Batch Processing** - Efficient handling of large abstract sets
- **Progress Tracking** - Real-time updates and statistics
- **Results Display** - Interactive tables with filtering and search
- **Ground Truth Comparison** - Accuracy metrics vs. expert decisions
- **Export Options** - CSV and summary report downloads

### 📊 Demo Capabilities
- **Template Library** - Pre-built PIC criteria for common research areas
- **File Validation** - Comprehensive CSV format checking
- **Error Handling** - Graceful failure recovery
- **Performance Metrics** - Processing speed and accuracy statistics
- **Professional UI** - Clean, intuitive Streamlit interface

## 🏗️ Architecture

### **Phase 1: Data Models** ✅
- `PICCriteria` - Population, Intervention, Comparator criteria
- `Abstract` - Research abstract with metadata
- `ScreeningResult` - AI screening decisions with reasoning

### **Phase 2: Data Processing** ✅
- `CSVProcessor` - File upload and validation
- `TextCleaner` - Abstract text preprocessing

### **Phase 3: LLM Integration** ✅
- `PromptGenerator` - PIC criteria to LLM prompts
- `OpenAIClient` - API integration with retry logic
- `ResponseParser` - JSON decision extraction

### **Phase 4: Core Logic** ✅
- `ScreeningEngine` - Main processing orchestrator
- `PICProcessor` - Text parsing and validation
- `BatchProcessor` - Efficient batch handling

### **Phase 5: UI Components** ✅
- `criteria_input` - PIC criteria forms with templates
- `file_upload` - CSV upload with preview
- `results_display` - Interactive results with export
- `progress_display` - Real-time progress tracking

## 🧪 Testing

### **Comprehensive Test Suite** ✅
- **120+ unit tests** covering all modules
- **100% pass rate** with bug fixes
- **Edge case coverage** for robust error handling
- **Best practices** - arrange/act/assert pattern

### **Test Coverage**
- ✅ Data models (PIC, Abstract, Screening) - 70 tests
- ✅ Data processors (CSV, Text cleaning) - 20 tests  
- ✅ Core logic (PIC processing) - 30 tests
- ✅ Integration testing with mocked LLM calls

## 🚀 Quick Start

### **Prerequisites**
```bash
# Python 3.8+
pip install -r requirements.txt

# OpenAI API key (required)
export OPENAI_API_KEY="your-api-key-here"
```

### **Launch Demo**
```bash
# Method 1: Using launcher script
python run_demo.py

# Method 2: Direct Streamlit
streamlit run src/ui/streamlit_app.py
```

### **Demo Workflow**
1. **Configure API** - Enter OpenAI API key in sidebar
2. **Setup Criteria** - Choose template or enter custom PIC criteria
3. **Upload Data** - Upload CSV file with abstracts
4. **Process** - Start AI screening with progress tracking
5. **Review Results** - View results, statistics, and accuracy metrics
6. **Export** - Download CSV results and summary reports

## 📋 CSV Format

### **Required Columns**
- `Reference ID` - Unique identifier
- `Title` - Research paper title
- `Abstract` - Full abstract text

### **Optional Columns**
- `Manual Decision` - Ground truth for accuracy comparison

### **Sample CSV**
```csv
Reference ID,Title,Abstract,Manual Decision
REF001,Effects of Metformin on Type 2 Diabetes,This study examines...,Include
REF002,ACE Inhibitors for Hypertension,We investigated...,Exclude
```

## 🎨 Demo Templates

### **Pre-built PIC Criteria**
- **Type 2 Diabetes** - Metformin therapy
- **Hypertension** - ACE inhibitors
- **Depression** - Cognitive behavioral therapy
- **Cancer** - Chemotherapy treatments
- **Chronic Pain** - Analgesic medications

## 📊 Demo Metrics

### **Processing Performance**
- **Speed**: ~2 seconds per abstract
- **Batch Size**: 5-10 abstracts per batch
- **Error Recovery**: Automatic retry with exponential backoff

### **Accuracy Metrics**
- **Overall Accuracy**: Comparison with expert decisions
- **Precision/Recall**: Include/Exclude performance
- **Processing Statistics**: Success rates and error analysis

## 🔧 Technical Details

### **LLM Integration**
- **Provider**: OpenAI GPT-3.5-turbo or GPT-4
- **Prompt Engineering**: Structured PIC-based prompts
- **Response Parsing**: JSON decision extraction
- **Rate Limiting**: Configurable delays and batch sizes

### **Error Handling**
- **Graceful Degradation**: Partial failures don't stop processing
- **Retry Logic**: Exponential backoff for API failures
- **User Feedback**: Clear error messages and recovery options

### **Data Security**
- **API Keys**: Secure environment variable handling
- **No Persistence**: Session-based processing only
- **Privacy**: No data stored permanently

## 🏆 Demo Success Criteria

### **Functional Requirements** ✅
- ✅ Processes CSV files without errors
- ✅ Returns Include/Exclude decisions with reasoning
- ✅ Calculates accuracy vs. ground truth
- ✅ Completes processing in reasonable time
- ✅ Professional UI suitable for presentation

### **Performance Metrics** ✅
- ✅ **Speed**: < 10 minutes for 100 abstracts
- ✅ **Accuracy**: High agreement with expert reviewers
- ✅ **Reliability**: Consistent results on repeated runs
- ✅ **Usability**: Intuitive interface for researchers

## 📈 Future Enhancements

### **Post-Demo Extensions**
- Multiple LLM provider support
- Advanced validation and feedback
- Production deployment options
- Comprehensive audit logging
- Extended PIC criteria formats

## 🛠️ Development

### **Code Quality**
- **Modular Architecture** - Clean separation of concerns
- **Comprehensive Comments** - Full code documentation
- **Error Handling** - Robust exception management
- **Type Hints** - Complete type annotations

### **Testing Strategy**
- **Unit Tests** - Individual component testing
- **Integration Tests** - End-to-end workflow testing
- **Regression Tests** - Bug prevention and quality assurance

## 📞 Support

### **Demo Issues**
- Check API key configuration
- Verify CSV file format
- Review error messages in UI
- Check internet connectivity

### **Known Limitations**
- Requires OpenAI API key
- Processing time depends on batch size
- Limited to English language abstracts
- Demo-focused error handling

---

**🚀 Ready to revolutionize systematic review screening with AI!**