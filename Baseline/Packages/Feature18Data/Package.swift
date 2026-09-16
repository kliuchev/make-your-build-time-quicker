// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature18Data",
    products: [.library(name: "Feature18Data", targets: ["Feature18Data"])],
    dependencies: [.package(path: "../Feature18Domain")],
    targets: [.target(name: "Feature18Data", dependencies: [.product(name: "Feature18Domain", package: "Feature18Domain")])]
)
