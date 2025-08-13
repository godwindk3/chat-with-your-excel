# Logging Setup Guide

## Overview
Enhanced logging has been added to help debug file deletion issues and track the complete file lifecycle.

## What's Added

### 1. Comprehensive Logging Configuration
- **File**: `app/core/logging_config.py`
- **Features**:
  - Daily log files in `logs/server_YYYY-MM-DD.log`
  - Console output with formatted messages
  - Different log levels for different components
  - Emoji indicators for easy visual scanning

### 2. Enhanced File Operations Logging
- **Upload**: Detailed tracking of file upload process
- **Delete**: Step-by-step deletion debugging with file system checks
- **Find**: Debug output when searching for files by ID

### 3. HTTP Request/Response Logging
- **All requests**: Method, URL, headers
- **Response timing**: How long each request takes
- **Status codes**: Success/failure tracking

## How to Use

### Start Server with Logging
```bash
cd chat-with-your-excel/back_end
python start_with_logs.py
```

### View Logs Real-time
```bash
# View current logs
python view_logs.py

# Follow logs in real-time (like tail -f)
python view_logs.py --follow
```

### Environment Setup
Create `.env` file in `back_end/` directory:
```env
FRONTEND_ORIGIN=http://localhost:5173
NGROK_ORIGIN=https://d6e27daed44c.ngrok-free.app
```

Create `.env` file in `front_end/` directory:
```env
VITE_API_BASE=https://09f57b9bbb56.ngrok-free.app/api
```

## What to Look For

### File Deletion Issues
When you get a 404 error deleting a file, check logs for:

1. **🗑️ DELETE FILE REQUEST** section shows:
   - File ID being requested
   - Files currently in storage
   - Whether the file was found by ID

2. **File path found: None** indicates:
   - File doesn't exist in storage
   - Frontend and backend are using different storage
   - File was already deleted

3. **Delete attempt X/3** shows:
   - Whether delete operations are succeeding
   - Any OS-level errors during deletion

### Ngrok Domain Mismatch
Look for different domains in:
- **🔄 DELETE /api/files/...** (request URL)
- **Headers: {'origin': '...'}** (frontend origin)

If these don't match your expected ngrok URLs, you have a domain mismatch.

### Double Requests
Look for two identical **🗑️ DELETE FILE REQUEST** entries with the same file ID close together - indicates double-clicking or multiple requests.

## Log File Locations
- **Daily logs**: `chat-with-your-excel/back_end/logs/`
- **File naming**: `server_2025-01-13.log`
- **Retention**: Manual cleanup (files don't auto-delete)

## Debug Commands
```bash
# Check if backend can see uploaded files
# Look for "Files in storage" in delete logs

# Check if file exists on disk
# Look for "File exists on disk: True/False"

# Verify ngrok setup
# Look for Origin header in request logs
```

## Common Issues & Solutions

### Issue: "File path found: None"
**Cause**: File doesn't exist in backend storage
**Check**: 
- Different ngrok URLs between upload and delete
- File was deleted by another process
- Wrong storage directory

### Issue: Multiple DELETE requests
**Cause**: Double-clicking delete button
**Solution**: Add button disabling (see frontend improvements)

### Issue: CORS errors in logs
**Cause**: Frontend origin not allowed by backend
**Solution**: Update `NGROK_ORIGIN` in backend `.env`
