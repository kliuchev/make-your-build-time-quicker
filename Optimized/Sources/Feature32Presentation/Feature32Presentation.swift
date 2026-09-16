import Feature32Domain
import Feature32Data

public enum Feature32PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature32DomainModel = Feature32DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
