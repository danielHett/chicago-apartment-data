import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import RefreshIcon from '@mui/icons-material/Refresh';
import FileDownloadIcon from '@mui/icons-material/FileDownload';

export default function StatisticsTable({ title, columns, rows }) {
  return (
    <>
      <Typography variant="h5" textAlign="center" sx={{ marginBottom: '10px' }}>
        {title}
      </Typography>
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} size="small">
          <TableHead>
            <TableRow sx={{ color: 'primary.main', backgroundColor: 'primary.main' }}>
              {columns.map((column, i) => {
                // if this is the first column, we don't align right!
                if (i === 0) return <TableCell color="primary">{column}</TableCell>;
                return (
                  <TableCell color="primary" align="right">
                    {column}
                  </TableCell>
                );
              })}
            </TableRow>
          </TableHead>
          <TableBody>{rows.map((row) => createRow(row, columns))}</TableBody>
        </Table>
      </TableContainer>
      <Box sx={{ display: 'flex', justifyContent: 'right', alignItems: 'center' }}>
        <IconButton children={<RefreshIcon fontSize="small" />} sx={{ borderRadius: 0 }} />
        <IconButton children={<FileDownloadIcon fontSize="small" />} sx={{ borderRadius: 0 }} />
      </Box>
    </>
  );
}

const createRow = (row, columns) => {
  return (
    <TableRow key={row.key} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
      {columns.map((column, i) => {
        let rowContent = '-';
        if (row[column]) rowContent = row[column];

        if (i === 0) return <TableCell>{rowContent}</TableCell>;
        return <TableCell align="right">{rowContent}</TableCell>;
      })}
    </TableRow>
  );
};
