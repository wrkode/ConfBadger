import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  CircularProgress,
  Alert,
  IconButton,
  InputAdornment,
  Tooltip,
} from '@mui/material';
import {
  Search as SearchIcon,
  Upload as UploadIcon,
  Download as DownloadIcon,
  Preview as PreviewIcon,
  Clear as ClearIcon,
  ContentCopy as CopyIcon,
} from '@mui/icons-material';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [file, setFile] = useState(null);
  const [resultFile, setResultFile] = useState(null);
  const [searchParams, setSearchParams] = useState({
    name: '',
    title: '',
    company: '',
    ticket_type: '',
  });
  const [attendees, setAttendees] = useState([]);
  const [badges, setBadges] = useState([]);
  const [participantdata, setParticipantData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  useEffect(() => {
    fetchBadges();
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchParams.name || searchParams.title || searchParams.company || searchParams.ticket_type) {
        handleSearch();
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [searchParams]);

  const fetchBadges = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/list-badges`);
      setBadges(response.data.badges);
    } catch (err) {
      setError('Failed to fetch badges');
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setFile(file);
    setLoading(true);
    setError(null);
    setSuccess(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post(`${API_BASE_URL}/upload-csv`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setSuccess('Badges generated successfully!');
      fetchBadges();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload file');
    } finally {
      setLoading(false);
    }
  };

  const handleFResultFileUpload = async (event) => {
    const resultFile = event.target.files[0];
    if (!resultFile) return;

    setResultFile(resultFile);
    setParticipantData([])
    const formData = new FormData();
    formData.append('file', resultFile);

    try {
      const response = await axios.post(`${API_BASE_URL}/upload-results-hash`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setSuccess('Result file uploaded!');
      console.log("Participant data received:", response.data.participantdata);
      setParticipantData(response.data.participantdata)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload file');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.get(`${API_BASE_URL}/search-attendees`, {
        params: searchParams,
      });
      setAttendees(response.data);
    } catch (err) {
      setError('Failed to search attendees');
    } finally {
      setLoading(false);
    }
  };

  const handleClearSearch = () => {
    setSearchParams({
      name: '',
      title: '',
      company: '',
      ticket_type: '',
    });
    setAttendees([]);
  };

  const handleClearCSV = () => {
    setResultFile(null)
    setParticipantData([]);
  };

  const handleDownloadBadge = async (attendee) => {
    // Convert Order # to string and remove decimal places
    const order = String(attendee['Order number']).split('.')[0];
    const badgeFilename = `${attendee['Last Name']}_${attendee['First Name']}_${order}.pdf`;
    window.open(`${API_BASE_URL}/badge/${badgeFilename}`, '_blank');
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Conference Badge Generator
      </Typography>

      <Paper sx={{ p: 3, mb: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Button
              variant="contained"
              component="label"
              startIcon={<UploadIcon />}
              fullWidth
            >
              Upload CSV File
              <input
                type="file"
                hidden
                accept=".csv"
                onChange={handleFileUpload}
              />
            </Button>
            {file && (
              <Typography variant="body2" sx={{ mt: 1 }}>
                Selected file: {file.name}
              </Typography>
            )}
          </Grid>

          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              label="Name"
              value={searchParams.name}
              onChange={(e) =>
                setSearchParams({ ...searchParams, name: e.target.value })
              }
              InputProps={{
                endAdornment: searchParams.name && (
                  <InputAdornment position="end">
                    <IconButton
                      size="small"
                      onClick={() => setSearchParams({ ...searchParams, name: '' })}
                    >
                      <ClearIcon />
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              label="Title"
              value={searchParams.title}
              onChange={(e) =>
                setSearchParams({ ...searchParams, title: e.target.value })
              }
              InputProps={{
                endAdornment: searchParams.title && (
                  <InputAdornment position="end">
                    <IconButton
                      size="small"
                      onClick={() => setSearchParams({ ...searchParams, title: '' })}
                    >
                      <ClearIcon />
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              label="Company"
              value={searchParams.company}
              onChange={(e) =>
                setSearchParams({ ...searchParams, company: e.target.value })
              }
              InputProps={{
                endAdornment: searchParams.company && (
                  <InputAdornment position="end">
                    <IconButton
                      size="small"
                      onClick={() => setSearchParams({ ...searchParams, company: '' })}
                    >
                      <ClearIcon />
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              label="Ticket Type"
              value={searchParams.ticket_type}
              onChange={(e) =>
                setSearchParams({ ...searchParams, ticket_type: e.target.value })
              }
              InputProps={{
                endAdornment: searchParams.ticket_type && (
                  <InputAdornment position="end">
                    <IconButton
                      size="small"
                      onClick={() => setSearchParams({ ...searchParams, ticket_type: '' })}
                    >
                      <ClearIcon />
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={12}>
            <Button
              variant="outlined"
              startIcon={<ClearIcon />}
              onClick={handleClearSearch}
              fullWidth
            >
              Clear Search
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {success}
        </Alert>
      )}

      {loading && (
        <Box display="flex" justifyContent="center" my={4}>
          <CircularProgress />
        </Box>
      )}

      {!loading && attendees.length === 0 && (searchParams.name || searchParams.title || searchParams.company || searchParams.ticket_type) && (
        <Alert severity="info" sx={{ mb: 2 }}>
          No attendees found matching your search criteria.
        </Alert>
      )}

      <Grid container spacing={3}>
        {attendees.map((attendee, index) => (
          <Grid item xs={12} md={6} lg={4} key={index}>
            <Card>
              <CardContent>
                <Typography variant="h6">
                  {attendee['First Name']} {attendee['Last Name']}
                </Typography>
                <Typography color="textSecondary">
                  {attendee['Job Title']}
                </Typography>
                <Typography variant="body2">
                  {attendee['Company']}
                </Typography>
                <Typography variant="body2">
                  {attendee['Email']}
                </Typography>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  startIcon={<PreviewIcon />}
                  onClick={() => handleDownloadBadge(attendee)}
                >
                  Preview Badge
                </Button>
                <Button
                  size="small"
                  startIcon={<DownloadIcon />}
                  onClick={() => handleDownloadBadge(attendee)}
                >
                  Download
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
      <Paper sx={{ p: 3, mb: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Button
              variant="contained"
              component="label"
              startIcon={<UploadIcon />}
              fullWidth
            >
              Upload Results File
              <input
                type="file"
                hidden
                accept=".csv"
                onChange={handleFResultFileUpload}
              />
            </Button>
            {resultFile && (
              <Typography variant="body2" sx={{ mt: 1 }}>
                Selected file: {resultFile.name}
              </Typography>
            )}
          </Grid>
          <Grid item xs={12}>
            <Button
              variant="outlined"
              startIcon={<ClearIcon />}
              onClick={handleClearCSV}
              fullWidth
            >
              Clear CSV
            </Button>
          </Grid>
        </Grid>
        <Grid container spacing={3}>
        {participantdata.length > 0 && (
          <Paper sx={{ p: 2, mt: 4 }}>
            <Typography variant="h6" gutterBottom>
              Raw CSV Output
            </Typography>
            <Tooltip title="Copy to clipboard">
              <IconButton
                onClick={() => {
                  const csvString = [
                    Object.keys(participantdata[0]).join(','),
                    ...participantdata.map((row) => Object.values(row).join(','))
                  ].join('\n');
                  navigator.clipboard.writeText(csvString);
                }}
              >
                <CopyIcon />
              </IconButton>
            </Tooltip>
            <Box
              component="pre"
              sx={{
                whiteSpace: 'pre-wrap',
                fontFamily: 'monospace',
                background: '#f5f5f5',
                padding: 2,
                borderRadius: 1,
                overflowX: 'auto',
              }}
            >
              {[
                Object.keys(participantdata[0]).join(','), // header
                ...participantdata.map((row) => Object.values(row).join(',')) // rows
              ].join('\n')}
            </Box>
          </Paper>
        )}
        </Grid>
      </Paper>
    </Container>
  );
}

export default App; 