// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature18Presentation",
    products: [.library(name: "Feature18Presentation", targets: ["Feature18Presentation"])],
    dependencies: [.package(path: "../Feature18Domain"),
        .package(path: "../Feature18Data")],
    targets: [.target(name: "Feature18Presentation", dependencies: [.product(name: "Feature18Domain", package: "Feature18Domain"), .product(name: "Feature18Data", package: "Feature18Data")])]
)
