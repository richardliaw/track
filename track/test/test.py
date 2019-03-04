import track


# Test 1
def test_track():
    def _save(data, fname):
        with open(fname, "w") as f:
            pickle.dump(data, f)


    def main_with_parser(args):
        for i in range(args.iters):
            track.metric(square=i*i)
            track.save(i**3, "hello.world", _save)

    track.init()
    main_with_cfg({"iters": 2})
    track.shutdown()


def test_tune_integration():
    def _save(data, fname):
        with open(fname, "w") as f:
            pickle.dump(data, f)

    def main_with_cfg(cfg):
        for i in range(cfg["iters"]):
            track.metric(square=i*i)
            track.save(i**3, "hello.world", _save)

    def reporter(**kwargs):
        print(kwargs)


    track.init(reporter=reporter)
    main_with_cfg({"iters": 2})
    track.shutdown()


def test_argparse_integration():
    raise NotImplementedError()

if __name__ == '__main__':
    test_track()
    test_tune_integration()
