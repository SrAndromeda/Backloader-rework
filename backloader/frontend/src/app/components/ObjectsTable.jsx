import {
    Box,
    Icon,
    IconButton,
    styled,
    Table,
    TableBody,
    TableCell,
    TableHead,
    TablePagination,
    TableRow,
} from "@mui/material";
import VisibilityIcon from '@mui/icons-material/Visibility';
import { useState } from "react";

const StyledTable = styled(Table)(() => ({
    whiteSpace: "pre",
    "& thead": {
        "& tr": { "& th": { paddingLeft: 0, paddingRight: 0 } },
    },
    "& tbody": {
        "& tr": { "& td": { paddingLeft: 0, textTransform: "capitalize" } },
    },
}));

const ObjectsTable = ({ headers, keyContent, content, pagination=false, paginationButtons=false, viewButton=false, viewAction=()=>{}, editButton=false, editAction=()=>{}, deleteButton=false, deleteAction=() => {} }) => {
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(5);
    const handleChangePage = (_, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(+event.target.value);
        setPage(0);
    };

    return (
        <Box width="100%" overflow="auto">
            <StyledTable>
                <TableHead>
                    <TableRow>
                        {headers
                            .map((header, index) => (
                                <TableCell key={index} align="center">{header}</TableCell>
                            ))
                        }
                    </TableRow>
                </TableHead>
                <TableBody>
                    {pagination
                        ? (content
                            .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                            .map((subscriber, index) => (
                                <TableRow key={index}>
                                    {keyContent
                                        .map((key, index2) => (
                                            <TableCell key={String(index)+"-"+String(index2)} align="center">{subscriber[key]}</TableCell>
                                        ))
                                    }
                                    {viewButton || editButton || deleteButton
                                        ? (<TableCell align="center">
                                            {viewButton
                                                && (<IconButton onClick={() => {viewAction(index)}}> <VisibilityIcon color="action" /> </IconButton>)
                                            }
                                            {editButton
                                                && (<IconButton onClick={() => {editAction(index)}}> <Icon color="secondary">edit</Icon> </IconButton>)
                                            }
                                            {deleteButton
                                                && (<IconButton onClick={() => {deleteAction(index)}}> <Icon color="error">delete</Icon> </IconButton>)
                                            }
                                        </TableCell>)
                                        : null
                                    }
                                </TableRow>
                            )))
                        : (content
                            .map((subscriber, index) => (
                                <TableRow key={index}>
                                    {keyContent
                                        .map((key, index2) => (
                                            <TableCell key={String(index)+"-"+String(index2)} align="center">{subscriber[key]}</TableCell>
                                        ))
                                    }
                                    {viewButton || editButton || deleteButton
                                        ? (<TableCell align="center">
                                            {viewButton
                                                && (<IconButton onClick={() => {viewAction(index)}}> <VisibilityIcon color="action" /> </IconButton>)
                                            }
                                            {editButton
                                                && (<IconButton onClick={() => {editAction(index)}}> <Icon color="secondary">edit</Icon> </IconButton>)
                                            }
                                            {deleteButton
                                                && (<IconButton onClick={() => {deleteAction(index)}}> <Icon color="error">delete</Icon> </IconButton>)
                                            }
                                        </TableCell>)
                                        : null
                                    }
                                </TableRow>
                            )))
                    }
                </TableBody>
            </StyledTable>
            {pagination && paginationButtons
                ? (<TablePagination
                    sx={{ px: 2 }}
                    page={page}
                    component="div"
                    rowsPerPage={rowsPerPage}
                    count={content.length}
                    onPageChange={handleChangePage}
                    rowsPerPageOptions={[5, 10, 25]}
                    onRowsPerPageChange={handleChangeRowsPerPage}
                    nextIconButtonProps={{ "aria-label": "Next Page" }}
                    backIconButtonProps={{ "aria-label": "Previous Page" }}
                />)
                : null
            }
            
        </Box>
    );
};

export default ObjectsTable;
