import { Box } from '@mui/material';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import useMediaQuery from '@mui/material/useMediaQuery';
import { useTheme } from '@mui/system';
import React from 'react';

export default function SimpleDialog({open, setOpen, title='', contentText='', handleClose=()=>{setOpen(false)}}) {
    // const [open, setOpen] = React.useState(false);
    const theme = useTheme();
    const fullScreen = useMediaQuery(theme.breakpoints.down('sm'));


    return (
        <Dialog
            fullScreen={fullScreen}
            open={open}
            onClose={handleClose}
            aria-labelledby="responsive-dialog-title"
        >
            <DialogTitle id="responsive-dialog-title">{title}</DialogTitle>

            <DialogContent>
                <DialogContentText>
                    {contentText}
                </DialogContentText>
            </DialogContent>

            <DialogActions>
                <Button onClick={handleClose} color="primary" autoFocus>
                    Ok
                </Button>
            </DialogActions>
        </Dialog>
    );
}
