import { useTheme } from '@mui/system';
import useMediaQuery from '@mui/material/useMediaQuery';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

function getQualityString(quality) {
    switch (quality) {
        case 'a':
            return 'Audio'
        case '720':
            return '720p'
        case '1080':
            return '1080p'
        case '1440':
            return '1440p'
        case '2160':
            return '4K'
        case 'max':
            return 'Best'
        default:
            return ''
    }
}

export default function ViewModal({open, setOpen, flow}){
    // const [open, setOpen] = React.useState(false);
    const theme = useTheme();
    const fullScreen = useMediaQuery(theme.breakpoints.down('sm'));

    function handleClose() {
        setOpen(false);
    }
    return (
        <>
            {flow != null
                ? (<Dialog
                    fullScreen={fullScreen}
                    fullWidth={fullScreen ? false : true}
                    maxWidth={'md'}
                    open={open}
                    onClose={handleClose}
                    aria-labelledby="responsive-dialog-title"
                >
                    <DialogTitle id="responsive-dialog-title">{flow.name}</DialogTitle>

                    <DialogContent>
                        <DialogContentText>
                            URL: <a href={flow.url}>Link</a>
                        </DialogContentText>
                        <DialogContentText>
                            Type: {flow.type == 'p' ? 'Playlist' : 'Channel'}
                        </DialogContentText>
                        <DialogContentText>
                            Quality: {getQualityString(flow.quality)}
                        </DialogContentText>
                        <DialogContentText>
                            Outlet: {flow.outlet.name}
                        </DialogContentText>
                        <DialogContentText>
                            TimerID: {flow.timer_id}
                        </DialogContentText>
                    </DialogContent>

                    <DialogActions>
                        <Button onClick={() => { setOpen(false) }} color="primary" autoFocus>
                            Ok
                        </Button>
                    </DialogActions>
                </Dialog>)
                : null
            }
        </>
    );
};