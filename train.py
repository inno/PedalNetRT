import pytorch_lightning as pl
import argparse

from model import PedalNet
from prepare import prepare


def main(args):
    """
    Trains the PedalNet model to match the output data from the input data.

    When you resume training from an existing model, you can override hparams
    such as max_epochs, batch_size, or learning_rate. Note that changing
    num_channels, dilation_depth, num_repeat, or kernel_size will change the
    shape of the WaveNet model and is not advised.

    """

    prepare(args)
    model = PedalNet(**vars(args))
    trainer = pl.Trainer(
        accelerator=args.accelerator,
        devices=args.devices,
        log_every_n_steps=args.log_every_n_steps,
        max_epochs=args.max_epochs,
    )
    if args.resume:
        trainer.fit(ckpt_path=args.model)
    else:
        trainer.fit(model)
    trainer.save_checkpoint(args.model)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file", nargs="?", default="data/in.wav")
    parser.add_argument("out_file", nargs="?", default="data/out.wav")
    parser.add_argument("--sample_time", type=float, default=100e-3)
    parser.add_argument("--normalize", type=bool, default=True)

    parser.add_argument("--num_channels", type=int, default=4)
    parser.add_argument("--dilation_depth", type=int, default=9)
    parser.add_argument("--num_repeat", type=int, default=2)
    parser.add_argument("--kernel_size", type=int, default=3)

    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--learning_rate", type=float, default=3e-3)

    parser.add_argument("--max_epochs", type=int, default=1000)
    parser.add_argument("--log_every_n_steps", type=int, default=100)

    parser.add_argument(
        "--accelerator",
        type=str,
        choices=["auto", "cpu", "ipu", "gpu", "tpu"],
        default="auto",
    )
    parser.add_argument("--devices", type=int, default=1)

    parser.add_argument(
        "--model",
        type=str,
        default="models/pedalnet/pedalnet.ckpt",
    )
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    main(args)
